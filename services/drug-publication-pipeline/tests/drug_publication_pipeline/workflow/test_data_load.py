from pathlib import Path
from unittest.mock import patch

from drug_publication_pipeline.workflow.data_load import save_output_data


@patch("drug_publication_pipeline.workflow.data_load.save_data_in_json_file")
@patch("drug_publication_pipeline.workflow.data_load.settings")
def test_save_output_data(mock_settings, mock_save_data_in_json_file):
    # Given
    mock_settings.return_value.output_json_file = Path("fake_output.json")
    mock_data = {
        "drug1": {
            "clinical_trials": [{"title": "Trial 1"}],
            "pubmeds": [{"title": "PubMed 1"}],
        }
    }

    # When
    save_output_data(mock_data)

    # Then
    mock_save_data_in_json_file.assert_called_once_with(
        mock_data, Path("fake_output.json")
    )
