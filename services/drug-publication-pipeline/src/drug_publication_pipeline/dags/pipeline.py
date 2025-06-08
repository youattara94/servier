import os
import sys
from datetime import datetime, timedelta

import pendulum
from airflow import DAG
from airflow.operators.python import PythonOperator

from drug_publication_pipeline.workflow.data_extract import load_input_data
from drug_publication_pipeline.workflow.data_load import save_output_data
from drug_publication_pipeline.workflow.data_transform.drug_mention_mapper import (
    find_drug_mentions,
    map_drugs_to_publications,
)
from drug_publication_pipeline.workflow.data_transform.validators import (
    get_clinical_trials_from_dataframes,
    get_drugs_from_dataframes,
    get_pubmeds_from_dataframes,
)

# Configuring Python path to help Airflow find the modules
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, "src"))

default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 6, 9, tzinfo=pendulum.timezone("Europe/Paris")),
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}


def extract_data(**context):
    input_data_dfs = load_input_data()
    context["ti"].xcom_push(key="input_data", value=input_data_dfs)


def transform_data(**context):
    # Extract input data from XCom
    input_data_dfs = context["ti"].xcom_pull(key="input_data", task_ids="extract_data")

    # Validate and extract objects from DataFrames
    # Any object that fails validation will be logged and skipped
    drugs = get_drugs_from_dataframes(input_data_dfs["drugs"])
    clinical_trials = get_clinical_trials_from_dataframes(
        input_data_dfs["clinical_trials"]
    )
    pubmeds = get_pubmeds_from_dataframes(input_data_dfs["pubmeds"])

    # Find drug mentions among the input files
    pubmeds_mentions = find_drug_mentions(drugs, pubmeds)
    clinical_trials_mentions = find_drug_mentions(drugs, clinical_trials)

    # Map drugs to their publication mentions
    drug_publication_mapping = map_drugs_to_publications(
        drugs, pubmeds_mentions, clinical_trials_mentions
    )
    context["ti"].xcom_push(key="output_data", value=drug_publication_mapping)


def load_data(**context):
    output_data = context["ti"].xcom_pull(key="output_data", task_ids="transform_data")
    save_output_data(output_data)


with DAG(
    dag_id="drug_publication_pipeline",
    default_args=default_args,
    schedule="@once",
    catchup=False,
) as dag:
    extract_task = PythonOperator(task_id="extract_data", python_callable=extract_data)
    transform_task = PythonOperator(
        task_id="transform_data", python_callable=transform_data
    )
    load_task = PythonOperator(task_id="load_data", python_callable=load_data)

    extract_task >> transform_task >> load_task
