import pandas as pd

from utils.unit_conversions import *
from method_lib.source_templates import nplanck_micron


class SourceModel:
    def __init__(
        self,
        sourceID: str = "default"
    ):
        self.sourceID = sourceID
        self.df = pd.DataFrame()

    def generateSourceData_BB(
            self,
            sourceSpectrum,
            sourceTemperature,
            unitsSI=False,
            showNPHOTONS=False,
            spectrum_unit: str = None
    ):

        if spectrum_unit is None:
            source_unit = detect_wavelength_unit(sourceSpectrum)
            if source_unit != "um":
                sourceSpectrum = convert_unit(
                    sourceSpectrum, from_unit=source_unit, to_unit="um")
                self.unit = "um"
        else:
            sourceSpectrum = convert_unit(
                sourceSpectrum, from_unit=source_unit, to_unit=spectrum_unit)
            self.unit = source_unit

        self.df['wavelength'] = sourceSpectrum
        self.df.set_index("wavelength", inplace=True)
        self.df[self.sourceID], _ = nplanck_micron(
            sourceSpectrum, sourceTemperature, SI=unitsSI, NPHOTONS=showNPHOTONS)
