import pandas as pd
import hashlib
from google.cloud import storage
import os

HASH_FILE_NAME = "data_hash.txt"  # File storing old hash

def hash_dataframe(df):
    """Generate a hash for a dataframe"""
    return hashlib.md5(pd.util.hash_pandas_object(df, index=True).values).hexdigest()




def get_old_hash(filename="hash.txt"):
    """Retrieve old hash value from a local file."""
    try:
        with open(filename, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None  # First-time run, no old hash


def save_new_hash(new_hash, filename="hash.txt"):
    """Save the new hash value to a local file."""
    with open(filename, "w") as f:
        f.write(new_hash)

