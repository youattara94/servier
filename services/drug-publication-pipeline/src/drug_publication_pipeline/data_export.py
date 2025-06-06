import json
from pathlib import Path


def write_json_file(
    data: dict[str, dict[str, list[dict[str, str]]]], output_file_path: str
) -> None:
    """
    Generates a JSON file from a dictionary containing drug publication references.
    """
    path_parent = Path(__file__).parent.parent.parent

    with open(path_parent / output_file_path, "w") as f:
        json.dump(data, f, indent=4)
