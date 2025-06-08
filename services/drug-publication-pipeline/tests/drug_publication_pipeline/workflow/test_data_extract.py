from unittest.mock import patch

import pandas as pd
from hamcrest import assert_that, equal_to, is_in

from drug_publication_pipeline.workflow.data_extract import load_input_data


@patch("drug_publication_pipeline.workflow.data_extract.load_data_file")
def test_load_input_data(mock_load_data_file, mock_settings):
    # Given
    mock_load_data_file.side_effect = lambda file_path: pd.DataFrame(
        {"mock_column": [f"data_from_{file_path.name}"]}
    )

    # When
    input_data_dfs = load_input_data()

    # Then
    # Check that the expected keys are in the dictionary
    assert_that("drugs", is_in(input_data_dfs))
    assert_that("clinical_trials", is_in(input_data_dfs))
    assert_that("pubmeds", is_in(input_data_dfs))

    # Check that the DataFrames contain the expected mock data
    assert_that(
        input_data_dfs["drugs"].iloc[0]["mock_column"],
        equal_to("data_from_fake_drugs.csv"),
    )
    assert_that(
        input_data_dfs["clinical_trials"].iloc[0]["mock_column"],
        equal_to("data_from_fake_clinical_trials.csv"),
    )
    assert_that(
        input_data_dfs["pubmeds"].iloc[0]["mock_column"],
        equal_to("data_from_fake_pubmed.csv"),
    )
    assert_that(
        input_data_dfs["pubmeds"].iloc[1]["mock_column"],
        equal_to("data_from_fake_pubmed.json"),
    )
