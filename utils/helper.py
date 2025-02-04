import pandas as pd
import hashlib
from google.cloud import storage

BUCKET_NAME = "status-0"
HASH_FILE_NAME = "data_hash.txt"  # File storing old hash

def hash_dataframe(df):
    """Generate a hash for a dataframe"""
    return hashlib.md5(pd.util.hash_pandas_object(df, index=True).values).hexdigest()



def get_old_hash():
    """Retrieve old hash value from Google Cloud Storage."""
    client = storage.Client()

    bucket = client.bucket(BUCKET_NAME)

    blob = bucket.blob(HASH_FILE_NAME)
    if blob.exists():
        return blob.download_as_text().strip()

    return None  # First-time run, no old hash


def save_new_hash(new_hash):
    """Save the new hash value to Google Cloud Storage after training."""
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(HASH_FILE_NAME)
    blob.upload_from_string(new_hash)
    blob = bucket.blob(HASH_FILE_NAME)
    blob.upload_from_string(new_hash)



