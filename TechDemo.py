from method_lib.telescope_model import TelescopeModel
from method_lib.source_model import SourceModel
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import utils.unit_conversions as uc

lambda_ = np.arange(0.201, 13, 0.001)


STEP_ = TelescopeModel("Simple_telescope")
STEP_.add_component("test_data/FB1750-500.xlsx", "FB17")

uc.convert_percentage(STEP_.df, "transmission")
STEP_.generate_throughput("transmission")

print(STEP_.df.head())

plt.plot(STEP_.df.index, STEP_.df["transmission_FB17"])
plt.plot(STEP_.df.index, STEP_.df["transmission_throughput"])
plt.show()

result = STEP_.map_spectrum(lambda_, "transmission_throughput")

sourceBB = SourceModel("Black Body")
sourceBB.generateSourceData_BB(lambda_, 5000, unitsSI=True)

result[sourceBB.sourceID] = sourceBB.df[sourceBB.sourceID]

# print(STEP_.metadata)
fig, ax = plt.subplots()

res = result.prod(axis=1)

ax.plot(result.index, result[sourceBB.sourceID], '--k')
ax.plot(result.index, res, 'k')
print(res)
ax.set_ylabel('transmission')
ax.set_xlabel('Wavelength [µm]')
plt.show()
