import pandas as pd


def load_excel_autoheader(path, max_scan_rows=10, min_nonempty_per_col=2):
    """
    Load an Excel file with unknown header position and padding columns.
    Automatically detects the header row and returns a clean DataFrame.
    """
    df = pd.read_excel(path, header=None)
    df = df.dropna(axis=1, how='all')

    sample = df.head(max_scan_rows)
    valid_cols = sample.columns[sample.notna().sum() >= min_nonempty_per_col]
    df = df[valid_cols]

    str_mask = df.applymap(lambda x: isinstance(x, str) and x.strip() != "")
    header_row_idx = str_mask.mean(axis=1).idxmax()

    header = [
        str(h).strip() if pd.notna(h) else f"Unnamed_{i}"
        for i, h in enumerate(df.iloc[header_row_idx])
    ]
    clean_df = df.iloc[header_row_idx + 1:].reset_index(drop=True)
    clean_df.columns = header
    clean_df = clean_df.loc[:, ~clean_df.columns.str.contains('^Unnamed')]
    clean_df = clean_df.apply(pd.to_numeric, errors='ignore')

    return clean_df
