import numpy as np


def make_spectrum_axis(start: float,
                       stop: float,
                       step: float,
                       precision: int = 9) -> np.ndarray:
    """
    Generate a high-precision wavelength axis using linspace
    with rounding to eliminate float-drift.

    Parameters
    ----------
    start : float
        Starting wavelength (inclusive)
    stop : float
        Ending wavelength (inclusive)
    step : float
        Step size between samples
    precision : int, optional
        Decimal rounding applied to stabilize floats.
        Default: 9

    Returns
    -------
    np.ndarray
        A clean, monotonic wavelength axis free of drift.
    """
    # Number of steps (inclusive)
    n = int(round((stop - start) / step)) + 1

    # Use linspace to avoid cumulative float drift
    axis = np.linspace(start, stop, n)

    # Round for safety
    return np.round(axis, precision)
