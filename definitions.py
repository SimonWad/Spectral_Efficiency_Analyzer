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
