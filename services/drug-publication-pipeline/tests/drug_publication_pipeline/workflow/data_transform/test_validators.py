import pandas as pd
from hamcrest import assert_that, equal_to

from drug_publication_pipeline.schemas.clinical_trial import ClinicalTrial
from drug_publication_pipeline.schemas.drug import Drug
from drug_publication_pipeline.schemas.pubmed import PubMed
from drug_publication_pipeline.workflow.data_transform.validators import (
    get_clinical_trials_from_dataframes,
    get_drugs_from_dataframes,
    get_pubmeds_from_dataframes,
)


def test_get_drugs_from_dataframes():
    # Given
    data = [
        {"id": "1", "name": "Aspirin"},
        {"id": "2", "name": "Ibuprofen"},
        {"name": "Paracetamol"},  # This will be skipped because 'id' is missing
    ]
    df = pd.DataFrame(data)

    # When
    drugs = get_drugs_from_dataframes(df)

    # Then
    assert_that(len(drugs), equal_to(2))
    assert_that(
        drugs, equal_to([Drug(id="1", name="Aspirin"), Drug(id="2", name="Ibuprofen")])
    )


def test_get_pubmeds_from_dataframes():
    # Given
    data = [
        {
            "id": 1,
            "title": "Aspirin reduces pain",
            "journal": "Medical Journal",
            "date": "2020-01-01",
        },
        {
            "id": 2,
            "title": "Ibuprofen for inflammation",
            "journal": "Clinical Trials Journal",
            "date": "2021-05-15",
        },
    ]
    df = pd.DataFrame(data)

    # When
    pubmeds = get_pubmeds_from_dataframes(df)

    # Then
    assert_that(len(pubmeds), equal_to(2))
    assert_that(
        pubmeds,
        equal_to(
            [
                PubMed(
                    id=1,
                    title="Aspirin reduces pain",
                    journal="Medical Journal",
                    publication_date="2020-01-01",
                ),
                PubMed(
                    id=2,
                    title="Ibuprofen for inflammation",
                    journal="Clinical Trials Journal",
                    publication_date="2021-05-15",
                ),
            ]
        ),
    )


def test_get_clinical_trials_from_dataframes():
    # Given
    data = [
        {
            "id": "CT1",
            "scientific_title": "Aspirin study",
            "journal": "Medical Journal",
            "date": "2020-01-01",
        },
        {
            "id": "CT2",
            "scientific_title": "Ibuprofen trial",
            "journal": "Clinical Trials Journal",
            "date": "2021-05-15",
        },
    ]
    df = pd.DataFrame(data)

    # When
    clinical_trials = get_clinical_trials_from_dataframes(df)

    # Then
    assert_that(len(clinical_trials), equal_to(2))
    assert_that(
        clinical_trials,
        equal_to(
            [
                ClinicalTrial(
                    id="CT1",
                    title="Aspirin study",
                    journal="Medical Journal",
                    publication_date="2020-01-01",
                ),
                ClinicalTrial(
                    id="CT2",
                    title="Ibuprofen trial",
                    journal="Clinical Trials Journal",
                    publication_date="2021-05-15",
                ),
            ]
        ),
    )
