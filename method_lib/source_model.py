import pandas as pd

from utils.unit_conversions import *
from method_lib.source_templates import nplanck_micron


class SourceModel:
    def __init__(
        self,
        wavelength_unit: str = "um",
        sourceID: str = "default"
    ):
        self.sourceID = sourceID
        self.df = pd.DataFrame()
        self.wavelength_unit = wavelength_unit
        self.unit = wavelength_unit

    def generateSourceData_BB(
            self,
            sourceSpectrum,
            sourceTemperature,
            unitsSI=False,
            showNPHOTONS=False,
            spectrum_unit: str = None
    ):
        if spectrum_unit is None:
            detected_unit = detect_wavelength_unit(sourceSpectrum)
        else:
            detected_unit = spectrum_unit

        if detected_unit != self.wavelength_unit:
            sourceSpectrum_converted = convert_unit(
                sourceSpectrum,
                from_unit=detected_unit,
                to_unit=self.wavelength_unit
            )
        else:
            sourceSpectrum_converted = sourceSpectrum

        sourceSpectrum_converted.astype(float).round(9)
        self.df = pd.DataFrame(index=sourceSpectrum_converted)
        bb_values, _ = nplanck_micron(
            sourceSpectrum_converted,
            sourceTemperature,
            SI=unitsSI,
            NPHOTONS=showNPHOTONS
        )
        self.df[self.sourceID] = bb_values
