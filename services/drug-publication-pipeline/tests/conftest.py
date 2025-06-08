from pathlib import Path
from unittest.mock import patch

import pytest


@pytest.fixture
def mock_settings():
    with patch(
        "drug_publication_pipeline.workflow.data_extract.settings"
    ) as mock_settings:
        mock_settings.return_value.drugs_csv_file = Path("fake_drugs.csv")
        mock_settings.return_value.clinical_trials_csv_file = Path(
            "fake_clinical_trials.csv"
        )
        mock_settings.return_value.pubmed_csv_file = Path("fake_pubmed.csv")
        mock_settings.return_value.pubmed_json_file = Path("fake_pubmed.json")
        yield mock_settings
