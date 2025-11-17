from method_lib import dataImporter as di
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as spi

lambda_ = np.arange(0.2, 13, 0.001)


# filterFB60 = di.OpticalComponentData("Bandpass Filter", "FB6000-500")
# filterFB60.readDataFromFile("test_data/FB6000-500.xlsx")

# filterE4 = di.OpticalComponentData("Flat Window", "E4_Broadband")
# filterE4.readDataFromFile("test_data/E4_Broadband_AR_Coating.xlsx")
# print(filterE4.header, "\n")

test = di.TelescopeModel("ME")
test.addComponent("test_data/FB6000-500.xlsx", "Filter", suffix="_FB60")
test.addComponent("test_data/FB1750-500.xlsx", "Filter", suffix="_FB17")
test.addComponent("test_data/FB6000-500.xlsx", "Filter", suffix="_FB60_2")

# plt.plot(filterFB60.df["wavelength"], filterFB60.df["transmission"], "k")
# plt.show()
# filterFB60.remap(lambda_, inplace=True, outputUnits=True)

# filterE4.remap(lambda_, inplace=True)

# # print(filterE4.df.head())

# plt.plot(filterFB60.df["wavelength"], filterFB60.df["transmission"], "--r")
# plt.show()
