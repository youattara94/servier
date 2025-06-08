import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings

# Path to directory `services/drug-publication-pipeline` relative to this file
SERVICE_ROOT_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    drugs_csv_file: Path = SERVICE_ROOT_DIR / "input/drugs.csv"
    pubmed_csv_file: Path = SERVICE_ROOT_DIR / "input/pubmed.csv"
    pubmed_json_file: Path = SERVICE_ROOT_DIR / "input/pubmed.json"
    clinical_trials_csv_file: Path = SERVICE_ROOT_DIR / "input/clinical_trials.csv"
    output_json_file: Path = (
        SERVICE_ROOT_DIR / "output/drug_mentions_in_publications.json"
    )

    class Config:
        env_file = ".env"


@lru_cache()
def settings() -> Settings:
    """
    Returns a cached instance of the Settings class.
    This allows for efficient access to configuration settings throughout the application.
    """
    return Settings()
