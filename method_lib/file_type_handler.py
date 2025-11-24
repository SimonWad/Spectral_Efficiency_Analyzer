import pandas as pd
import numpy as np
import os
import re
import warnings
import pickle
from definitions import *
from method_lib.source_templates import *


def load_excel_autoheader(path, max_scan_rows=10, min_nonempty_per_col=2):
    """
    Load an Excel file with unknown header position and padding columns.
    Automatically detects the header row and returns a clean DataFrame.
    """
    # 1. Load all data without assuming a header
    df = pd.read_excel(path, header=None)

    # 2. Drop columns that are entirely empty
    df = df.dropna(axis=1, how='all')

    # 3. Use only the first few rows to identify valid columns
    sample = df.head(max_scan_rows)
    valid_cols = sample.columns[sample.notna().sum() >= min_nonempty_per_col]
    df = df[valid_cols]

    # 4. Find the header row: the one with the most string-like entries
    # pandas >= 2.2 prefers .map over .applymap
    try:
        str_mask = df.map(lambda x: isinstance(x, str) and x.strip() != "")
    except AttributeError:
        # fallback for older pandas versions (<2.2)
        str_mask = df.applymap(
            lambda x: isinstance(x, str) and x.strip() != "")

    header_row_idx = str_mask.mean(axis=1).idxmax()

    # 5. Build the final DataFrame
    header = [
        str(h).strip() if pd.notna(h) else f"Unnamed_{i}"
        for i, h in enumerate(df.iloc[header_row_idx])
    ]
    clean_df = df.iloc[header_row_idx + 1:].reset_index(drop=True)
    clean_df.columns = header

    # 6. Remove empty "Unnamed" columns
    clean_df = clean_df.loc[:, ~clean_df.columns.str.contains('^Unnamed')]

    # 7. Attempt numeric conversion where possible
    clean_df = clean_df.apply(pd.to_numeric)

    return clean_df


def detectCompatible(fileName):
    supportedFileTypes = [".csv", ".xlsx", ".xls", ".txt", ".json"]
    _, ext = os.path.splitext(fileName)
    ext = ext.lower()

    if ext not in supportedFileTypes:
        raise ValueError(
            f"Unsupported file type: '{ext}'. Supported types are: {', '.join(supportedFileTypes)}")
    return True, ext
