from utils.helper import hash_dataframe

from mage_ai.settings.repo import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_big_query(*args, **kwargs):
    """
    Template for loading data from a BigQuery warehouse.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#bigquery
    """
    query = 'SELECT DISTINCT * FROM `weather-data-pipeline-442718.weather_dataset.buraidah`'
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    df = BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).load(query)
    new_hash = hash_dataframe(df)
    return new_hash


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
