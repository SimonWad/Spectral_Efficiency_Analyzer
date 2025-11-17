from method_lib import dataImporter as di
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

lambda_ = np.arange(0.2, 13, 0.001)


filterFB17 = di.OpticalComponentData()
filterFB17.readDataFromFile("test_data/FB1750-500.xlsx")


filter_df = filterFB17.remap(lambda_)
print(filter_df.head())

sourceBB = di.OpticalComponentData(
    typeID="source", storageID="Black Body 5000 K", isSource=True)
sourceBB.generateSourceData_BB(lambda_, 5000, unitsSI=True, showNPHOTONS=True)

fig, (ax1, ax2) = plt.subplots(2, 1)

ax1.plot(lambda_, sourceBB.df[sourceBB.storageID], 'k')
ax1.set_ylabel(f"$[{sourceBB.units}]$")

ax2.plot(lambda_, filter_df['transmission'], 'k')
ax2.set_ylabel('transmission [%]')
ax2.set_xlabel('Wavelengt [µm]')
plt.show()

resultingData = pd.DataFrame()
resultingData[f"Wavelength ({sourceBB.detect_wavelength_unit(lambda_)})"] = lambda_

resultingData["Effeciency"] = sourceBB.df[sourceBB.storageID] * \
    (filter_df['transmission'] / 100)


plt.plot(lambda_, resultingData["Effeciency"], 'k')
plt.plot(lambda_, sourceBB.df[sourceBB.storageID], '--k')
plt.xlabel('Wavelengt [µm]')
plt.ylabel(f"$[{sourceBB.units}]$")
plt.show()
