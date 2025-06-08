import logging
from pathlib import Path

import pandas as pd

from drug_publication_pipeline.settings import settings
from drug_publication_pipeline.utils import load_data_file


def load_input_data() -> dict[str, pd.DataFrame]:
    """
    Load data in "input" directory into a dictionary of DataFrames.
    """
    input_file_paths = {
        "drugs": settings().drugs_csv_file,
        "clinical_trials": settings().clinical_trials_csv_file,
        "pubmed_csv": settings().pubmed_csv_file,
        "pubmed_json": settings().pubmed_json_file,
    }

    logging.info("Loading input data from files...")
    drugs_df = load_data_file(input_file_paths["drugs"])
    clinical_trials_df = load_data_file(input_file_paths["clinical_trials"])
    pubmed_csv_df = load_data_file(input_file_paths["pubmed_csv"])
    pubmed_json_df = load_data_file(input_file_paths["pubmed_json"])
    all_pubmed_df = pd.concat([pubmed_csv_df, pubmed_json_df], ignore_index=True)
    logging.info("Input data loaded successfully")

    input_data_dfs = {
        "drugs": drugs_df,
        "clinical_trials": clinical_trials_df,
        "pubmeds": all_pubmed_df,
    }
    return input_data_dfs
