from mage_ai.orchestration.run_status_checker import check_status

if 'sensor' not in globals():
    from mage_ai.data_preparation.decorators import sensor
from utils.helper import get_old_hash

@sensor
def check_condition(new_hash, *args, **kwargs) -> bool:
    """
    Sensor function to check if new data is available by comparing hashes.
    Also checks if the pipeline run is complete.
    """

    old_hash = get_old_hash()  # Fetch old hash from GCS

    # First-time run or new data detected
    if old_hash is None or new_hash != old_hash:
        return True  # Trigger pipeline

    # If no new data, check pipeline run status
    return check_status(
        'pipeline_uuid',
        kwargs.get('execution_date'),
        block_uuid='block_uuid',
        hours=24
    )
