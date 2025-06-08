from hamcrest import assert_that, equal_to

from drug_publication_pipeline.schemas.clinical_trial import ClinicalTrial
from drug_publication_pipeline.schemas.drug import Drug
from drug_publication_pipeline.schemas.pubmed import PubMed
from drug_publication_pipeline.workflow.data_transform.drug_mention_mapper import (
    find_drug_mentions,
    map_drugs_to_publications,
)


def test_find_drug_mentions():
    # Given
    drugs = [Drug(id="1", name="Aspirin"), Drug(id="2", name="Ibuprofen")]
    publications = [
        PubMed(
            id=1,
            title="Aspirin reduces pain",
            journal="Medical Journal",
            publication_date="2020-01-01",
        ),
        ClinicalTrial(
            id="CT1",
            title="Ibuprofen for inflammation",
            journal="Clinical Trials Journal",
            publication_date="2021-05-15",
        ),
        PubMed(
            id=2,
            title="Paracetamol study",
            journal="Health Journal",
            publication_date="2019-12-31",
        ),
    ]

    # When
    mentions = find_drug_mentions(drugs, publications)

    # Then
    assert_that(len(mentions), equal_to(2))
    assert_that(
        mentions,
        equal_to(
            [
                {
                    "drug": "Aspirin",
                    "title": "Aspirin reduces pain",
                    "journal": "Medical Journal",
                    "date": "2020-01-01",
                },
                {
                    "drug": "Ibuprofen",
                    "title": "Ibuprofen for inflammation",
                    "journal": "Clinical Trials Journal",
                    "date": "2021-05-15",
                },
            ]
        ),
    )


def test_map_drugs_to_publications():
    # Given
    drugs = [Drug(id="1", name="Aspirin"), Drug(id="2", name="Ibuprofen")]
    pubmed_mentions = [
        {
            "drug": "Aspirin",
            "title": "Aspirin reduces pain",
            "journal": "Medical Journal",
            "date": "2020-01-01",
        },
    ]
    clinical_trials_mentions = [
        {
            "drug": "Ibuprofen",
            "title": "Ibuprofen for inflammation",
            "journal": "Clinical Trials Journal",
            "date": "2021-05-15",
        },
    ]

    # When
    mapping = map_drugs_to_publications(
        drugs, pubmed_mentions, clinical_trials_mentions
    )

    # Then
    assert_that(
        mapping,
        equal_to(
            {
                "Aspirin": {
                    "pubmed_publications": [
                        {"title": "Aspirin reduces pain", "date": "2020-01-01"}
                    ],
                    "scientific_publications": [],
                    "journals": [{"journal": "Medical Journal", "date": "2020-01-01"}],
                },
                "Ibuprofen": {
                    "pubmed_publications": [],
                    "scientific_publications": [
                        {"title": "Ibuprofen for inflammation", "date": "2021-05-15"}
                    ],
                    "journals": [
                        {"journal": "Clinical Trials Journal", "date": "2021-05-15"}
                    ],
                },
            }
        ),
    )
