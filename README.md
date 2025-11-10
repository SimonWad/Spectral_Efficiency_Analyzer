# Spectral Efficiency Analyzer (SEA)

This library provides a set of functions for analyzing the spectral efficiency of select optical components. These components can be filters, lens coatings or thin films. Anything that can be modelled by an efficiency curve or an Optical Density curve.

Each provided data file is stored as an object and serialized in a local cache. The Object definitions is found in the method_lib/dataImporter file.

## Requirements

The required packages are:

- pandas
- matplotlib
- numpy

All requirements are found in the `requirements.txt`

```bash
pip install -r requirements.txt
```

From a terminal in the project directory.

> **_For versions of python before 3.9_**

You need to install the pickle library, this is used to serialize the data object.

```bash
pip install pickle
```

## method_lib/

This folder contains the python files that define every relevant method.

Currently there is two files:

- `dataImporter.py`
- `SourceTemplateFuncs.py`

`dataImporter.py`, despite the name handles both imports and exports of the data provided by the user. Any file you want to use as either efficiency data or source data is defined as an object. Then serialized using the pickle library.

This library contains other usefull functions. General use is shown as an example in `TechDemo.py`.¹

> It is recommended to import the library and rename it. Rename it to your hearts desire.

```python
import method_lib.dataImporter as di
```

¹Do look at the files for a better idea of the process. I have tried to be as descriptive as possible. Each class is explained in definition.

`sourceTemplateFuncs.py`is the location for the source functions. Currently there is only one, it generates a planck spectrum from a given wavelength range and a temperature in kelvin [K]. There is two modifiers, you can ask for SI units or Photon flux. When the object sourceObject is initialized. Call the method

```python
myObj.generateSourceData_BB(sourceSpectrum, sourceTemperature, unitsSI=bool, showNPHOTONS=bool)
```

**_Be aware that the current state of the software does not easily allow for custom ranges in the SourceSpectrum..._**

**_For ease of use I recommend using the wavelengths from the efficiency data._**

## Bugs or errors

If any bugs occur that is not easily fixed. Please reach out, I will look into them and fix for next update.

## Feature ideas.

- Dynamic unit change
- GUI for data input
- SQLite for database
