import pickle
import os
import json

import pandas as pd

from method_lib.telescope_model import TelescopeModel
from definitions import ROOT_DIR


def save_telescope_model(
        telescope_model: TelescopeModel,
        filename: str
):
    tel = telescope_model
    dir = ROOT_DIR
    os.makedirs(dir+"/Telescope_models/", exist_ok=True)
    path = os.path.join(dir, "Telescope_models/", filename)
    data = {
        "Metadata": tel.metadata,
        "Telescope Dataframe": json.loads(tel.df.to_json(orient="index"))
    }

    with open(path, "w") as file:
        json.dump(data, file, indent=4)


def load_telescope(filename):
    path = os.path.join(dir, "Telescope_models/", filename)
    with open(path, "r") as file:
        data = json.load(file)

    df = pd.DataFrame.from_dict(data["Telescope Dataframe"], orient="index")
    metadata = data["Metadata"]

    return df, metadata


def save_pickled_telescope(obj, filename):
    """Save any Python object to a pickle file."""
    dir = ROOT_DIR
    os.makedirs(dir+"/Telescope_models/", exist_ok=True)
    path = os.path.join(dir, "Telescope_models/", filename)

    with open(path, 'wb') as f:
        pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)


def load_pickled_telescope(filename):
    """Load and return a Python object from a pickle file."""
    path = os.path.join(dir, "Telescope_models/", filename)
    with open(path, 'rb') as f:
        return pickle.load(f)
