import io
import pandas as pd
import requests
from mage_ai.data_preparation.shared.secrets import get_secret_value

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    api_key = get_secret_value('API_KEY')
    loc  = 'Buraidah'

    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{loc}/next7days?key={api_key}&include=days&unitGroup=uk&elements=datetime,tempmax,tempmin,temp,feelslike'
    response = requests.get(url).json()
    df = pd.DataFrame(response['days'])    
    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
