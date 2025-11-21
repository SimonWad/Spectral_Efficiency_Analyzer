import pandas as pd
import numpy as np
import re
from scipy.interpolate import interp1d

from definitions import *
from method_lib.source_templates import *
from method_lib.file_type_handler import *
from method_lib.data_importer import read_data_file
from utils.unit_conversions import *


class TelescopeModel:
    def __init__(
            self,
            ID: str = "default_telescope"
    ):
        self.ID = ID
        self.df = pd.DataFrame()
        self.__temp_df = pd.DataFrame()
        self.metadata = {
            "Telescope ID": self.ID,
            "components": [],
            "units": {},  # standardized column -> unit (e.g. '%' or 'nm')
            "wavelength_axis": None,
            "spectral_bounds": None,
            "spectral_unit": None,
        }

    '''
    Main methods:
        Component adding
    '''

    def add_component(
            self,
            filePath: str,
            componentID: str,
            suffix: str = None
    ):
        # Make sure that the method returns a DataFrame
        self.__temp_df = self._load_component(filePath)
        self.standardize_header(self.__temp_df)
        self.__temp_df.set_index("wavelength", inplace=True)

        if suffix is None:
            generated_suffix = "_" + componentID
            self.__temp_df = self.__temp_df.add_suffix(
                generated_suffix, axis=1)
            self.metadata["components"].append(generated_suffix)
        else:
            self.__temp_df = self.__temp_df.add_suffix(suffix, axis=1)
            self.metadata["components"].append(suffix)

        if self.df.empty:
            self.df = self.__temp_df.copy()
            self._update_metadata()

        else:
            self.__temp_df = self.__temp_df.reindex(
                self.metadata["wavelength_axis"]).interpolate()
            self.df = pd.concat([self.df, self.__temp_df], axis=1)
            self._update_metadata()

    def generate_throughput(
            self,
            target: str
    ):
        contains_target = self.df.columns.str.contains(target)
        fetched_cols = self.df.loc[:, contains_target].columns.values
        self.df[target + "_throughput"] = self.df[fetched_cols].prod(axis=1)

    def map_spectrum(
            self,
            lambda_,
            througput_col: str,
            method: str = "linear"
    ) -> pd.DataFrame:
        telescope_axis_unit = detect_wavelength_unit(self.df.index)
        input_axis_unit = detect_wavelength_unit(lambda_)
        conv_lambda_ = convert_unit(lambda_, from_unit=input_axis_unit,
                                    to_unit=telescope_axis_unit)
        f = interp1d(self.df.index, self.df[througput_col], kind=method)

        result_df = pd.DataFrame(index=lambda_, data=f(
            conv_lambda_), columns=["Throughput"])
        self.mapped_throughput_df = result_df.copy()
        return result_df

    '''
    Testing methods
    '''

    def _load_component(
            self,
            path: str
    ) -> pd.DataFrame:
        df = read_data_file(path)
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Reader must return a pandas DataFrame.")
        return df.copy()

    '''
    Methods for header processing 
    '''

    def _detect_unit_in_header(self, header: str):
        raw = header.strip()
        lower = raw.lower()
        detected_unit = None
        cleaned = raw

        # 1. Detect unit from definitions.py → UNIT_KEYWORDS
        for pattern, unit in UNIT_KEYWORDS:
            if re.search(pattern, lower):
                detected_unit = UNIT_NORMALIZATION.get(unit, unit)
                cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
                break

        # 2. Strip tokens
        for tok in HEADER_STRIP_TOKENS:
            cleaned = cleaned.replace(tok, "")

        cleaned = cleaned.strip().strip("-").strip("_").lower()

        return cleaned, detected_unit

    def parse_header_list(self, headers: list[str]):
        """
        Processes a list of column headers.
        Returns:
            cleaned_headers : list[str]
            detected_units  : dict[str, str or None]
        """
        cleaned_headers = []
        detected_units = {}

        for h in headers:
            clean, unit = self._detect_unit_in_header(h)
            cleaned_headers.append(clean)
            detected_units[clean] = unit

        return cleaned_headers, detected_units

    def standardize_header(self, input_df):
        if input_df.empty:
            raise ValueError(
                "Cannot standardize headers of an empty DataFrame.")

        headers = list(input_df.columns)

        # Step 1: parse header list
        cleaned_headers, detected_units = self.parse_header_list(headers)
        # Step 2: rename columns in dataframe
        rename_map = {old: new for old, new in zip(headers, cleaned_headers)}

        input_df.rename(columns=rename_map, inplace=True)

        # Step 3: update class metadata
        self.header_units = detected_units
        self.header = cleaned_headers
        self.metadata["units"] = detected_units

        # Step 4: alias mapping (using ALIAS_MAP)
        for key, patterns in ALIAS_MAP.items():
            setattr(self, f"has_{key}", False)

        for h in cleaned_headers:
            for std_name, patterns in ALIAS_MAP.items():
                if any(re.search(p, h) for p in patterns):
                    setattr(self, f"has_{std_name}", True)

        return rename_map

    '''
    Metadata processing
    '''

    def _update_metadata(self):
        axis = self.metadata.get("wavelength_axis")
        if axis is None:
            if self.df.empty:
                return
            axis = self.df.index
        axis = pd.Index(axis.astype(float), name="wavelength")
        self.metadata["wavelength_axis"] = axis
        self.metadata["spectral_bounds"] = (
            float(axis.min()), float(axis.max()))
        self.metadata["spectral_unit"] = detect_wavelength_unit(
            axis)
