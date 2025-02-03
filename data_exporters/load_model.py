

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

from pandas import DataFrame
from sklearn.pipeline import Pipeline
import os
import pickle
from pydantic import BaseModel

with open(f'{os.getcwd()}/finalized_model.lib', 'rb') as m:
    model = pickle.load(m)


@data_exporter
def export_data(*args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    # Specify your data exporting logic here
    print(model)

