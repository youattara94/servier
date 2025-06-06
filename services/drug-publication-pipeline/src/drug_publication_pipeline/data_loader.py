from pathlib import Path

import pandas as pd


def read_file(file_path: str) -> pd.DataFrame:
    """
    Reads a file and returns a pandas DataFrame based on the file extension.
    """
    path_parent = Path(__file__).parent.parent.parent

    if file_path.endswith(".csv"):
        return pd.read_csv(path_parent / file_path, dtype=str)
    elif file_path.endswith(".json"):
        return pd.read_json(path_parent / file_path, dtype=str)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")
