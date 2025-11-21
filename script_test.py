from method_lib.telescope_model import TelescopeModel
from method_lib.source_model import SourceModel

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import utils.unit_conversions as uc


lambda_ = np.arange(0.201, 13, 0.001)

test = TelescopeModel()
test.add_component("test_data/FB6000-500.xlsx", "Filter", suffix="_FB60")
test.add_component("test_data/FB1750-500.xlsx", "Filter", suffix="_FB17")
# test.addComponent("test_data/FB6000-500.xlsx", "Filter", suffix="_FB60_2")

uc.convert_percentage(test.df, "transmission")
test.generate_throughput("transmission")

plt.plot(test.df.index, test.df["transmission_FB17"])
plt.plot(test.df.index, test.df["transmission_FB60"])
plt.plot(test.df.index, test.df["transmission_throughput"])
plt.show()

result = test.map_spectrum(lambda_, "transmission_throughput")

source = SourceModel("BlackBody")
source.generateSourceData_BB(lambda_, 5000, unitsSI=True)

result[source.sourceID] = source.df[source.sourceID]

res = result.prod(axis=1)

plt.plot(result.index, result["Throughput"])
print(res)
plt.show()
