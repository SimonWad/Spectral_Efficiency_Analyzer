import unittest
from method_lib.data_importer import TelescopeModel


class Test_TestDetectUnitsInHeader(unittest.TestCase):

    def test_headerInput(
            self,
    ):
        test_obj = TelescopeModel()
        test_header = ["wavelength (nm)", "wavelength (µm)",
                       "Transmission %", "Optical Density OD"]
        expected_result = ["nm", "um", "%", ""]
        assert test_obj._detect_units_in_header(
            header=test_header) == expected_result
