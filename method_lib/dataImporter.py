import pandas as pd
import numpy as np
import os
import re
import warnings
import pickle
from definitions import *
from method_lib.sourceTemplateFuncs import *
from scipy.interpolate import interp1d
from method_lib.FileTypeHandler import *


def readDataFile(fileName, txtDelim=None) -> pd.DataFrame:
    _, fileType = detectCompatible(fileName)

    match fileType:
        case ".csv":
            df = pd.read_csv(fileName)
        case ".xlsx":
            df = load_excel_autoheader(fileName)
        case ".txt":
            if txtDelim is None:
                txtDelim = input('Please indicate delimiter: ')
            df = pd.read_table(fileName, delimiter=txtDelim, header=0)
        case _:
            raise ValueError(
                f"File type is not supported yet..."
            )
    if df.isnull().values.any() > 0:
        warnings.warn("Beware, the dataframe contains missing values")
    return df


def detect_data_start(df, numeric_threshold=0.8):
    for i, row in df.iterrows():
        numeric_fraction = np.mean(pd.to_numeric(row, errors="coerce").notna())
        if numeric_fraction >= numeric_threshold:
            return i
    return 0


def storeEfficiencyData(dataObj: object, cachePath: str = "dataCache/"):
    with open(cachePath + dataObj.name + '_EFFICIENCY_DATA.pickle', 'wb') as f:
        pickle.dump(dataObj, f, pickle.HIGHEST_PROTOCOL)


def storeSourceData(dataObj: object, cachePath: str = "dataCache/", generateDataFile: bool = False):
    with open(cachePath + dataObj.sourceID + '_SOURCE.pickle', 'wb') as f:
        pickle.dump(dataObj, f, pickle.HIGHEST_PROTOCOL)
    if generateDataFile is True:
        fileName = dataObj.sourceID + ".csv"
        with open(fileName, "wb") as file:
            dataObj.df.to_csv(file)


def loadStoredObject(fileName: str):
    with open(fileName, "rb") as f:
        data = pickle.load(f)
    return data


class OpticalComponentData:
    """
    A class for defining optical components present in a system, this calss is a universal data configuration.

    init:
    There is asked for several information pieces.
        - typeID, which is the ID for the optical element or source. This can be whatever, 'filter' for optical filters, 'coating' for surface coating on lenses, 'black body' if the component is a source.

        - StorageID, the name of the component. Here you are also spoiled with choice. This parameter defines the storage name so be descriptive.

        - isSource, a boolean that defines if the type is a source or not.

    """

    def __init__(
            self,
            typeID: str = "unknown",
            storageID: str = "unknown",
            isSource: bool = False
    ) -> pd.DataFrame:

        self.typeID = typeID
        self.storageID = storageID
        self.df = pd.DataFrame()
        self.isSource = isSource

    def generateSourceData_BB(
            self,
            sourceSpectrum,
            sourceTemperature,
            unitsSI=False,
            showNPHOTONS=False
    ):

        if self.isSource is True:
            self.df = pd.DataFrame()
            self.df['Wavelength (µm)'] = sourceSpectrum
            self.df[self.storageID], self.units = nplanck_micron(
                sourceSpectrum, sourceTemperature, SI=unitsSI, NPHOTONS=showNPHOTONS)
        if not self.isSource:
            raise TypeError(
                "Object is not defined as a source. Please set isSource = True")

    def addUserDefinedData(
            self,
            spectrum_data: np.ndarray | pd.DataFrame,
            efficiency_data: np.ndarray | pd.DataFrame,
            spectrum_col_label: str = "wavelength",
            efficiency_col_label: str = "efficiency data"
    ):
        # Convert numpy arrays to DataFrames if necessary
        if isinstance(spectrum_data, np.ndarray):
            spectrum_data = pd.DataFrame(spectrum_data, columns=[
                                         spectrum_col_label])
        if isinstance(efficiency_data, np.ndarray):
            efficiency_data = pd.DataFrame(efficiency_data, columns=[
                                           efficiency_col_label])

        self.df[spectrum_col_label] = spectrum_data
        self.df[efficiency_col_label] = efficiency_data
        self.header = self.getHeader()

    def readDataFromFile(
            self,
            dataFileName: str
    ):

        self.df = readDataFile(os.path.join(ROOT_DIR, dataFileName))
        self.standardize_header()
        self.header = self.getHeader()
        print(self.df.head())

    def getHeader(
            self
    ):
        return list(self.df.columns.values)

    def remap(
            self,
            newWavelengths: np.ndarray | pd.DataFrame,
            method: str = "linear",
            inplace=False,
            outputUnits: bool = False
    ):

        header = self.getHeader()  # update in case of data changes
        dataWavelengths = self.df[header[0]]

        # Normalize the both spectrums
        unit_data = self.detect_wavelength_unit(dataWavelengths)
        unit_lambda_ = self.detect_wavelength_unit(newWavelengths)

        if unit_data != unit_lambda_:
            dataWavelengths = self.convert_unit(
                dataWavelengths, unit_data, unit_lambda_)
        if outputUnits:
            print("Starting unit for the spectrum data: \n", unit_data, "\n")
            print("Unit of the new spectrum: \n", unit_lambda_, "\n")
            print("Spectrum unit after normalization: \n",
                  self.detect_wavelength_unit(newWavelengths), "\n")

        tol_factor = 1e-3  # relative tolerance: 0.1% of lower bound
        unit_step = tol_factor * dataWavelengths.min()  # scales with wavelength

        lower_diff = abs(newWavelengths.min() - dataWavelengths.min())

        if lower_diff > unit_step:
            warnings.warn(
                f"\nLower input boundary {newWavelengths.min():.4f} differs from data boundary "
                f"{dataWavelengths.min():.4f} by {lower_diff:.4g} (> tolerance {unit_step:.4g}). "
                f"Possible extrapolation or regression errors.\n"
            )

        # Detect which columns exist
        has_OD = len(header) > 2
        dataValues = self.df[header[1]]
        dataOD = self.df[header[2]] if has_OD else None

        print(
            f"Interpolating: {dataWavelengths.name} → {header[1]}{' + ' + header[2] if has_OD else ''}")

        # Validate wavelength data
        if np.any(np.isnan(dataWavelengths)):
            raise ValueError("NaN values found in wavelength column.")
        if np.any(np.diff(dataWavelengths) <= 0):
            raise ValueError(
                "Wavelengths must be strictly increasing for interpolation.")

        # Interpolate
        f = interp1d(dataWavelengths, dataValues,
                     kind=method, fill_value="extrapolate")
        newValues = f(newWavelengths)

        if has_OD:
            g = interp1d(dataWavelengths, dataOD, kind=method,
                         fill_value="extrapolate")
            newOD = g(newWavelengths)

        # Build new DataFrame safely
        new_df_data = {
            header[0]: newWavelengths,
            header[1]: newValues
        }
        if has_OD:
            new_df_data[header[2]] = newOD

        new_df = pd.DataFrame(new_df_data)

        # Handle in-place vs return
        if inplace:
            self.df = new_df.reset_index(drop=True)
            return self
        else:
            return new_df

    def normalize_wavelengths(
            self,
            wavelengths: pd.DataFrame | np.ndarray,
            unit: bool = None,
            default_unit: str = "nm",
            autodetect: bool = True
    ):
        if unit is None:
            if autodetect:
                unit = self.detect_wavelength_unit(wavelengths)
            else:
                unit = default_unit
        return self.convert_unit(wavelengths, unit)

    def detect_wavelength_unit(
            self,
            wavelengths: pd.DataFrame | np.ndarray
    ):

        mean_val = np.mean(wavelengths)
        if mean_val > 1e5:
            return "angstrom"
        elif mean_val > 100:
            return "nm"
        elif mean_val < 10:
            return "um"
        else:
            return "m"  # rare case

    def convert_unit(
            self,
            values: pd.DataFrame | np.ndarray,
            from_unit: str,
            to_unit: str = "um"
    ):
        """
        Convert wavelength array between arbitrary units.
        """

        from_unit = from_unit.lower()
        to_unit = to_unit.lower()

        if from_unit not in UNIT_TO_METERS:
            raise ValueError(f"Unsupported input unit: {from_unit}")
        if to_unit not in UNIT_TO_METERS:
            raise ValueError(f"Unsupported output unit: {to_unit}")

        # Convert everything through meters
        values_in_m = values * UNIT_TO_METERS[from_unit]
        return values_in_m / UNIT_TO_METERS[to_unit]

    def standardize_header(
            self
    ):
        """
        Standardizes dataframe headers for optical data and sets capability flags.
        """
        if self.df.empty:
            raise ValueError(
                "DataFrame is empty. Load data before standardizing headers.")

        rename_map = {}
        lowered = [col.lower().strip() for col in self.df.columns]

        # Initialize detection flags
        for key in ALIAS_MAP.keys():
            setattr(self, f"has_{key}", False)

        # Try to match each column
        for original, col_lower in zip(self.df.columns, lowered):
            for std_name, patterns in ALIAS_MAP.items():
                if any(re.search(p, col_lower) for p in patterns):
                    rename_map[original] = std_name
                    setattr(self, f"has_{std_name}", True)
                    break  # stop after first match to avoid overwriting

        # Apply renaming safely
        if rename_map:
            self.df.rename(columns=rename_map, inplace=True)
            self.header = list(self.df.columns)
        else:
            print("Warning: No known optical headers detected.")

        return rename_map
