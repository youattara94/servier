from drug_publication_pipeline.settings import settings
from drug_publication_pipeline.utils import save_data_in_json_file


def save_output_data(data: dict[str, dict[str, list[dict[str, str]]]]) -> None:
    """
    Generates a JSON file from a dictionary containing drug publication mentions.
    """
    output_file_path = settings().output_json_file
    save_data_in_json_file(data, output_file_path)
