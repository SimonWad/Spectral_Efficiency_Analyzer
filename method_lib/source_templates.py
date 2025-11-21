import numpy as np
from utils.unit_conversions import *


def nplanck_micron(lambda_micron, temp, SI=False, NPHOTONS=False):
    """
    Calculate the Planck function in units of:
      - erg/cm^2/s/µm (default)
      - W/m^2/µm if SI=True
      - photon flux if NPHOTONS=True

    Parameters
    ----------
    lambda_micron : float or array-like
        Wavelength(s) in microns (µm).
    temp : float
        Temperature in Kelvin.
    SI : bool, optional
        If True, output is in SI units W/m^2/µm. Default is False (erg/cm^2/s/µm).
    NPHOTONS : bool, optional
        If True, return photon number flux (N/cm^2/s/µm or N/m^2/s/µm).

    Returns
    -------
    bbflux : ndarray
        Blackbody flux or photon flux at each wavelength.

    Example: 0.2 to 2.9 µm range for 30,000 K blackbody

    lam_um = np.arange(0.2, 3.0, 0.1)
    temp = 30000

    bbflux = nplanck_micron(lam_um, temp)
    print(bbflux)

    """

    lam = np.atleast_1d(lambda_micron).astype(np.float64)
    lam_unit = detect_wavelength_unit(lam)
    if lam_unit is not "um":
        lam = convert_unit(lam, from_unit=lam_unit, to_unit="um")

    # Constants (in cgs units, same as before)
    c1 = 3.741773e-5      # 2hc^2  [erg*cm^2/s]
    c2 = 1.438777         # hc/k   [cm*K]
    c3 = 1.986446e-16     # hc     [erg*cm]

    # Convert wavelength from µm → cm
    w = lam * 1e-4

    # Compute exponential term
    val = c2 / (w * temp)

    # Avoid floating overflow (IDL equivalent good_lim = 88–308)
    good = val < 308
    bbflux = np.zeros_like(w)

    # Planck function (π * Iλ) in erg/cm^2/s/cm
    bbflux[good] = c1 / (w[good]**5 * (np.exp(val[good]) - 1.0))

    # Convert per cm to per µm
    bbflux *= 1e-4  # because 1 µm = 1e-4 cm

    # Unit conversions and photon option
    if NPHOTONS:
        if SI:
            bbflux = 1e-4 * bbflux * w / c3   # photons/m^2/s/µm
            units = "photons/m^2/s/µm"
        else:
            bbflux = 1e-8 * bbflux * w / c3   # photons/cm^2/s/µm
            units = "photons/cm^2/s/µm"
    else:
        if SI:
            bbflux = 1e-11 * bbflux           # W/m^2/µm
            units = "W/m^2/µm"
        else:
            bbflux = 1e-8 * bbflux            # erg/cm^2/s/µm
            units = "erg/cm ^ 2/s/µm"

    bbflux[bbflux < 1e-24] = 0.0

    return (bbflux, units) if np.ndim(lambda_micron) > 0 else bbflux.item()
