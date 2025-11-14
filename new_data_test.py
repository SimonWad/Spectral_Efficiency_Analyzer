from method_lib import dataImporter as di
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

idx = "wavelength"

FB17 = di.OpticalComponentData()
FB17.readDataFromFile("test_data/FB1750-500.xlsx")
FB17.standardize_header()
FB17.df.set_index(idx, inplace=True)
FB17.df.sort_index(inplace=True)

E4 = di.OpticalComponentData()
E4.readDataFromFile("test_data/E4_Broadband_AR_Coating.xlsx")
E4.standardize_header()
print(FB17.df.index)
E4.normalize_wavelengths(FB17.df.index)
E4.df.set_index(idx, inplace=True)
E4.df.sort_index(inplace=True)

# Now align E4 to FB17:
E4.df = E4.df.reindex(FB17.df.index).interpolate(method='linear')
print(E4.df)


