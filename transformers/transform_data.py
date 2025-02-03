import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    data['datetime'] = pd.to_datetime(data['datetime'])
    data['day_of_week'] = data['datetime'].dt.day_name()
    data['temp_range'] = data['tempmax'] - data['tempmin']
    data.rename(columns={"datetime": "date_time", "tempmax": "max_temp", "tempmin": "min_temp",'feelslike': 'feels_like'}, inplace=True)
    return data [['date_time', 'day_of_week', 'temp', 'min_temp','max_temp','feels_like','temp_range']]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
