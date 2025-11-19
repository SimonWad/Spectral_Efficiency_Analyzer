import pandas as pd
import numpy as np

from definitions import *


def convert_unit(
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


def normalize_wavelengths(
        wavelengths: pd.DataFrame | np.ndarray,
        unit: bool = None,
        default_unit: str = "nm",
        autodetect: bool = True
):
    if unit is None:
        if autodetect:
            unit = detect_wavelength_unit(wavelengths)
        else:
            unit = default_unit
    return convert_unit(wavelengths, unit)


def detect_wavelength_unit(
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


def convert_percentage(
        df: pd.DataFrame,
        percentage_flag: str
):
    contains_target = df.columns.str.contains(percentage_flag)
    fetched_cols = df.loc[:, contains_target].columns.values
    df[fetched_cols] = df[fetched_cols] / 100
