from method_lib.telescope_model import TelescopeModel
from method_lib.source_model import SourceModel
from method_lib.read_write_data_models import *

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import utils.unit_conversions as uc
from utils.index_diagnostics import *
from utils.spectrum_axis import *


lambda_ = make_spectrum_axis(0.200, 13, 0.001, 9)


STEP_ = TelescopeModel("um", "Simple_telescope")
# STEP_.add_component("test_data/FGL280.xls", "FGL280")
STEP_.add_component("test_data/ZnSe_Window_Data.xlsx", "ZnSe_Window")
# STEP_.add_component("test_data/ZnSe_Window_Data.xlsx", "TWO_ZnSe")
STEP_.add_component("test_data/FGL280.xls", "FGL280")
print(STEP_.metadata)

uc.convert_percentage(STEP_.df, "transmission")
STEP_.generate_throughput("transmission")

print(STEP_.df)

plt.plot(STEP_.df.index, STEP_.df["transmission_FGL280"])
plt.plot(STEP_.df.index, STEP_.df["transmission_ZnSe_Window"])
plt.plot(STEP_.df.index, STEP_.df["transmission_throughput"])
# plt.show()

result = STEP_.map_spectrum(lambda_, "transmission_throughput")

sourceBB = SourceModel("um", "Black Body")
sourceBB.generateSourceData_BB(lambda_, 5000, unitsSI=True)
sourceBB.df.index.astype(float).round(9)
print(sourceBB.df)

sourceBB.df.index = sourceBB.df.index.astype(float)

index_diagnostic(result.index, sourceBB.df.index)

source_col = sourceBB.df[sourceBB.sourceID].reindex(result.index)

result[sourceBB.sourceID] = source_col

print(result)

save_telescope_model(STEP_, "test_model_data.json")


# # print(STEP_.metadata)
# fig, ax = plt.subplots()

# res = result.prod(axis=1)

# ax.plot(result.index, result[sourceBB.sourceID], '--k')
# ax.plot(result.index, res, 'k')
# print(result)
# print(res)
# ax.set_ylabel('transmission')
# ax.set_xlabel('Wavelength [µm]')
# plt.show()
