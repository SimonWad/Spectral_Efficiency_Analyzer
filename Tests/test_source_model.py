import unittest
import numpy as np
import pandas as pd
from unittest.mock import patch

from method_lib.source_model import SourceModel


class TestSourceModel(unittest.TestCase):

    @patch("method_lib.source_model.nplanck_micron")
    @patch("method_lib.source_model.detect_wavelength_unit")
    @patch("method_lib.source_model.convert_unit")
    def test_generate_source_bb_no_conversion(
        self,
        mock_convert,
        mock_detect_unit,
        mock_nplanck
    ):
        # Fake detection: say input is already in "um"
        mock_detect_unit.return_value = "um"

        # convert_unit should not be called because units already match
        mock_convert.side_effect = lambda x, **_: x

        # Mock nplanck_micron output
        mock_nplanck.return_value = (np.array([10.0, 20.0, 30.0]), None)

        src = SourceModel(wavelength_unit="um", sourceID="BB")

        # Input spectrum already in microns
        spectrum = np.array([1.0, 2.0, 3.0])

        src.generateSourceData_BB(
            sourceSpectrum=spectrum,
            sourceTemperature=5000
        )

        # ---- Assertions ----
        # 1. DataFrame index is set correctly
        self.assertTrue(np.allclose(src.df.index.to_numpy(), spectrum))

        # 2. Column exists
        self.assertIn("BB", src.df.columns)

        # 3. Values from mocked Planck function are used
        self.assertTrue(np.allclose(src.df["BB"].values, [10.0, 20.0, 30.0]))

        # 4. convert_unit should NOT have been called
        mock_convert.assert_not_called()

    @patch("method_lib.source_model.nplanck_micron")
    @patch("method_lib.source_model.detect_wavelength_unit")
    @patch("method_lib.source_model.convert_unit")
    def test_generate_source_bb_with_conversion(
        self,
        mock_convert,
        mock_detect,
        mock_nplanck
    ):
        src = SourceModel(wavelength_unit="um", sourceID="BB")

        # Input is in nanometers
        input_spectrum = np.array([500, 600, 700])

        # Mock detection says "nm", so conversion required
        mock_detect.return_value = "nm"

        # Fake conversion output (500nm → 0.5um etc.)
        converted = np.array([0.5, 0.6, 0.7])
        mock_convert.return_value = converted

        # Return fake Planck values
        mock_nplanck.return_value = (np.array([1.0, 2.0, 3.0]), None)

        src.generateSourceData_BB(
            sourceSpectrum=input_spectrum,
            sourceTemperature=3000
        )

        # ---- Assertions ----
        # convert_unit MUST be called
        mock_convert.assert_called_once()

        # Index must use converted values
        self.assertTrue(np.allclose(src.df.index.values, converted))

        # Planck values added
        self.assertTrue(np.allclose(src.df["BB"].values, [1.0, 2.0, 3.0]))

    @patch("method_lib.source_model.nplanck_micron")
    @patch("method_lib.source_model.convert_unit")
    def test_generate_source_bb_custom_spectrum_unit(
        self,
        mock_convert,
        mock_nplanck
    ):
        src = SourceModel(wavelength_unit="um", sourceID="Star")

        # input values
        spectrum = np.array([1000, 2000])  # treat as nm

        # simulate conversion
        mock_convert.return_value = np.array([1.0, 2.0])

        # mock Planck values
        mock_nplanck.return_value = (np.array([8.0, 9.0]), None)

        src.generateSourceData_BB(
            sourceSpectrum=spectrum,
            sourceTemperature=4000,
            spectrum_unit="nm"   # override detection
        )

        # ---- Assertions ----
        mock_convert.assert_called_once()

        # correct converted index
        self.assertTrue(np.allclose(src.df.index.values, [1.0, 2.0]))

        # correct brightness
        self.assertTrue(np.allclose(src.df["Star"].values, [8.0, 9.0]))

    @patch("method_lib.source_model.nplanck_micron")
    def test_generate_source_bb_units_match_no_conversion(self, mock_nplanck):

        src = SourceModel(wavelength_unit="um")

        spectrum = np.array([1.1, 1.2, 1.3])

        mock_nplanck.return_value = (np.array([5, 6, 7]), None)

        src.generateSourceData_BB(spectrum, 6000)

        self.assertTrue(np.allclose(src.df.index, spectrum))
        self.assertTrue(np.allclose(src.df["default"], [5, 6, 7]))
