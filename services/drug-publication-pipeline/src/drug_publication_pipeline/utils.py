import json
import logging
from pathlib import Path

import pandas as pd


def load_data_file(file_path: Path) -> pd.DataFrame:
    """
    Loads data in a file and returns a pandas DataFrame based on the file extension
    """
    # Mapping extensions to Pandas read functions
    pd_readers = {
        ".csv": pd.read_csv,
        ".json": pd.read_json,
    }

    file_extension = file_path.suffix.lower()
    reader = pd_readers.get(file_extension)

    if reader is None:
        raise ValueError(f"Unsupported file extension: {file_extension}")

    try:
        return reader(file_path, dtype=str, encoding="utf-8")  # type: ignore[operator]
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"File is empty: {file_path}")
    except pd.errors.ParserError:
        raise ValueError(f"Error parsing the file: {file_path}")
    except Exception as e:
        raise RuntimeError(
            f"Unexpected error while reading the file '{file_path}': {e}"
        ) from e


def save_data_in_json_file(
    data: dict[str, dict[str, list[dict[str, str]]]], output_file_path: str
) -> None:
    """Save data into a JSON file"""
    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        logging.info(f"Data saved to {output_file_path}")
