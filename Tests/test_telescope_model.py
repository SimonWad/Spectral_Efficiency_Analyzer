import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch

from method_lib.telescope_model import TelescopeModel


class TestTelescopeModel(unittest.TestCase):

    def setUp(self):
        self.telescope = TelescopeModel(wavelength_unit="nm")

        # sample component DF
        self.sample_df = pd.DataFrame({
            "wavelength": [500, 510, 520],
            "reflectance %": [0.8, 0.85, 0.9]
        })

    # -----------------------------
    # Header detection
    # -----------------------------

    def test_detect_unit_in_header(self):
        clean, unit = self.telescope._detect_unit_in_header("Reflectance (%)")
        self.assertEqual(clean, "reflectance")
        self.assertEqual(unit, "%")

    def test_standardize_header(self):
        df = self.sample_df.copy()
        self.telescope.standardize_header(df)

        self.assertListEqual(list(df.columns), ["wavelength", "reflectance"])
        self.assertEqual(self.telescope.metadata["units"]["reflectance"], "%")

    # -----------------------------
    # add_component with mocking
    # -----------------------------

    @patch("method_lib.telescope_model.read_data_file")
    def test_add_component(self, mock_reader):
        mock_reader.return_value = self.sample_df.copy()

        self.telescope.add_component("dummy.txt", "mirror")

        # New column exists
        cols = self.telescope.df.columns
        self.assertIn("reflectance_mirror", cols)

        # Component registered
        self.assertEqual(self.telescope.metadata["components"], ["_mirror"])

        # Index is float precision
        self.assertIsInstance(self.telescope.df.index[0], float)

    # -----------------------------
    # Throughput generation
    # -----------------------------

    def test_generate_throughput(self):
        self.telescope.df = pd.DataFrame({
            "mirror_a": [0.8, 0.9],
            "mirror_b": [0.5, 0.6],
        }, index=[500.0, 510.0])

        self.telescope.generate_throughput("mirror")

        expected = np.array([0.4, 0.54])
        actual = self.telescope.df["mirror_throughput"].values

        self.assertTrue(np.allclose(expected, actual))

    # -----------------------------
    # Spectrum mapping / interpolation
    # -----------------------------

    def test_map_spectrum(self):
        self.telescope.df = pd.DataFrame({
            "mirror_throughput": [0.4, 0.6, 0.8]
        }, index=[500, 550, 600])

        result = self.telescope.map_spectrum(
            lambda_=[520, 560],
            througput_col="mirror_throughput",
            method="linear"
        )

        self.assertAlmostEqual(result.loc[520, "Throughput"], 0.48, places=6)
        self.assertAlmostEqual(result.loc[560, "Throughput"], 0.64, places=6)


if __name__ == "__main__":
    unittest.main()
