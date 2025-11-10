import pandas as pd
import numpy as np
import os
import warnings
import pickle
from definitions import *
from method_lib.sourceTemplateFuncs import *


def detectCompatible(fileName):
    supportedFileTypes = [".csv", ".xlsx", ".txt", ".json"]
    _, ext = os.path.splitext(fileName)
    ext = ext.lower()

    if ext not in supportedFileTypes:
        raise ValueError(
            f"Unsupported file type: '{ext}'. Supported types are: {', '.join(supportedFileTypes)}")

    return True, ext


def readDataFile(fileName, txtDelim=None) -> pd.DataFrame:
    _, fileType = detectCompatible(fileName)

    match fileType:
        case ".csv":
            df = pd.read_csv(fileName)
        case ".xlsx":
            df = pd.read_excel(fileName)
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
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


class efficiencyData:
    """
    A class for storing effieciency data:

    dataFileName: str
    The path to the datafile relative to the library directory

    type: str
    A string defining what the type of effieciency data is. 
    eg. Filter, surface coating, prism, lens, ...

    name: str
    The name of the effiecency data. recommended is to use the product name or product number for easy reference.
    """

    def __init__(self, dataFileName: str, type: str, name: str) -> pd.DataFrame:
        self.df = readDataFile(os.path.join(ROOT_DIR, dataFileName))
        self.type = type
        self.name = name
        self.header = self.getHeader()

    def getHeader(self):
        return list(self.df.columns.values)


class sourceData:

    """
    A class for storing and generatng source Data:

    sourceID: str
    The name for your source. It can be anything really. Saved datafiles will be named with this ID so be descriptive.
    """

    def __init__(self, sourceID: str):
        self.sourceID = sourceID

    def generateSourceData_BB(self, sourceSpectrum, sourceTemperature, unitsSI=False, showNPHOTONS=False):
        self.df = pd.DataFrame()
        self.df['Wavelength (µm)'] = sourceSpectrum
        self.df[self.sourceID], self.units = nplanck_micron(
            sourceSpectrum, sourceTemperature, SI=unitsSI, NPHOTONS=showNPHOTONS)
