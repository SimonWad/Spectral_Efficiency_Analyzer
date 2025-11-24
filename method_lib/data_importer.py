import pandas as pd
import numpy as np
import warnings
from definitions import *
from method_lib.source_templates import *
from method_lib.file_type_handler import *


def read_data_file(
        fileName,
        txtDelim=None
) -> pd.DataFrame:
    _, fileType = detectCompatible(fileName)

    match fileType:
        case ".csv":
            df = pd.read_csv(fileName)
        case ".xlsx" | ".xls":
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


def detect_data_start(
        df,
        numeric_threshold=0.8
):
    for i, row in df.iterrows():
        numeric_fraction = np.mean(pd.to_numeric(row, errors="coerce").notna())
        if numeric_fraction >= numeric_threshold:
            return i
    return 0
