import os
ROOT_DIR = os.path.dirname(os.path.abspath(
    __file__))

UNIT_TO_METERS = {
    "m": 1.0,         # meters
    "cm": 1e-2,       # centimeters
    "mm": 1e-3,       # millimeters
    "um": 1e-6,       # micrometers
    "µm": 1e-6,       # micrometers (unicode version)
    "nm": 1e-9,       # nanometers
    "angstrom": 1e-10  # angstroms
}

HEADER_TARGETS = {
    "wavelength": ["wave", "wl", "λ", "lambda"],
    "frequency": ["freq", "hz", "ω", "nu"],
    "transmission": ["trans", "t%", "transm", "transmit", "intensity"],
    "reflection": ["refl", "r%", "mirror", "reflectance"],
    "absorption": ["abs", "a%", "loss"],
    "optical_density": ["od", "dens", "optical d", "o.d"],
    "refractive_index_n": ["n", "refractive", "real(n)"],
    "refractive_index_k": ["k", "imag(n)", "extinction"],
    "angle": ["angle", "aoi", "incident", "theta", "φ", "polar", "azimuth"],
    "polarization": ["pol", "s-pol", "p-pol", "ellipticity", "retardance"],
    "intensity": ["intensity", "radiance", "irradiance", "flux", "power"],
    "temperature": ["temp", "t (°c)", "thermal"],
}

ALIAS_MAP = {
    "wavelength":      [r"\bwav", r"\blambda", r"λ", r"wl"],
    "frequency":       [r"\bfreq", r"\bω", r"\bnu"],
    "transmission":    [r"\btrans", r"\bt%", r"\btransm", r"\bintensity"],
    "reflection":      [r"\brefl", r"\br%", r"\bmirror", r"\breflectance"],
    "absorption":      [r"\babs", r"\ba%", r"\bloss"],
    "optical_density": [r"\bod", r"\bdens", r"\boptical.?d"],
    "n":               [r"\bn\s*(\(real\))?", r"refractive", r"\breal\(n\)"],
    "k":               [r"\bk\s*(\(imag\))?", r"\bextinction", r"\bimag\(n\)"],
    "angle":           [r"\bangle", r"\baoi", r"\bincident", r"θ", r"phi", r"azimuth"],
    "polarization":    [r"\bpol", r"\bs-pol", r"\bp-pol", r"\bellipticity", r"\bretard"],
    "intensity":       [r"\bintensity", r"\bradiance", r"\birradiance", r"\bflux", r"\bpower"],
    "temperature":     [r"\btemp", r"°c", r"thermal"],
}
