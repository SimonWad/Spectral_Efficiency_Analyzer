# Spectral Efficiency Analyzer (SEA)

This library provides a set of functions for analyzing the spectral efficiency of select optical components. These components can be filters, lens coatings or thin films. Anything that can be modelled by an efficiency curve or an Optical Density curve.

Each provided data file is stored in a telescope model containing a pandas dataframe. The contained data will be marked with a suffix that identifies that specific component.

Telescope models can be saved in a JSON format containing the dataframe and the accumilated metadata.

## Requirements

All requirements are found in the `requirements.txt`

```bash
pip install -r requirements.txt
```

From a terminal in the project directory.

## Bugs or errors

If any bugs occur that is not easily fixed. Please reach out, I will look into them and fix for next update.

## Feature ideas.

- Dynamic unit change
- GUI for data input
- SQLite for database
