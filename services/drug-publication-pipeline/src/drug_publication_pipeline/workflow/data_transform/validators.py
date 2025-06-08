import logging

import pandas as pd
from pydantic import ValidationError

from drug_publication_pipeline.schemas.clinical_trial import ClinicalTrial
from drug_publication_pipeline.schemas.drug import Drug
from drug_publication_pipeline.schemas.pubmed import PubMed


def get_drugs_from_dataframes(df: pd.DataFrame) -> list[Drug]:
    """Validate and extracts Drug objects from a DataFrame."""
    drugs: list[Drug] = []
    for _, drug in df.iterrows():
        try:
            drugs.append(Drug(**drug.to_dict()))
        except ValidationError as e:
            logging.error(f"Skipping Drug entry '{drug.to_dict()}' : {e}")
    return drugs


def get_pubmeds_from_dataframes(df: pd.DataFrame) -> list[PubMed]:
    """Validate and extracts PubMed objects from a DataFrame."""
    pubmeds: list[PubMed] = []
    for _, pubmed in df.iterrows():
        try:
            pubmeds.append(PubMed(**pubmed.to_dict()))
        except ValidationError as e:
            logging.error(f"Skipping PubMed entry '{pubmed.to_dict()}' : {e}")
    return pubmeds


def get_clinical_trials_from_dataframes(df: pd.DataFrame) -> list[ClinicalTrial]:
    """Validate and extracts ClinicalTrial objects from a DataFrame."""
    clinical_trials: list[ClinicalTrial] = []
    for _, clinical_trial in df.iterrows():
        try:
            clinical_trials.append(ClinicalTrial(**clinical_trial.to_dict()))
        except ValidationError as e:
            logging.error(
                f"Skipping Clinical Trial entry '{clinical_trial.to_dict()}' : {e}"
            )
    return clinical_trials
