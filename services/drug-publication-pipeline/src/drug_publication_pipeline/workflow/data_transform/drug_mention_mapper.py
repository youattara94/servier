import pandas as pd

from drug_publication_pipeline.schemas.clinical_trial import ClinicalTrial
from drug_publication_pipeline.schemas.drug import Drug
from drug_publication_pipeline.schemas.pubmed import PubMed


def find_drug_mentions(
    drugs: list[Drug], publications: list[PubMed] | list[ClinicalTrial]
) -> list[dict[str, str]]:
    """Finds mentions to drugs from a list of PubMed or clinical trials."""
    mentions = []
    for drug in drugs:
        drug_name = drug.name.lower()
        for pub in publications:
            if drug_name in pub.title.lower():
                mentions.append(
                    {
                        "drug": drug.name,
                        "title": pub.title,
                        "journal": pub.journal,
                        "date": pub.publication_date.isoformat(),
                    }
                )
    return mentions


def map_drugs_to_publications(
    drugs: list[Drug],
    pubmed_mentions: list[dict[str, str]],
    clinical_trials_mentions: list[dict[str, str]],
) -> dict[str, dict[str, list[dict[str, str]]]]:
    """
    Maps drugs to their mentions in PubMed and clinical trials, including journal information
    """
    mapping: dict[str, dict[str, list[dict[str, str]]]] = {}

    # Initialize mapping structure
    for drug in drugs:
        drug_name = drug.name
        mapping[drug_name] = {
            "pubmed_publications": [],
            "scientific_publications": [],
            "journals": set(),
        }

    # Add PubMed mentions
    for ref in pubmed_mentions:
        drug = ref["drug"]
        mapping[drug]["pubmed_publications"].append(
            {"title": ref["title"], "date": ref["date"]}
        )
        mapping[drug]["journals"].add((ref["journal"], ref["date"]))

    # Add clinical trials mentions
    for ref in clinical_trials_mentions:
        drug = ref["drug"]
        mapping[drug]["scientific_publications"].append(
            {"title": ref["title"], "date": ref["date"]}
        )
        mapping[drug]["journals"].add((ref["journal"], ref["date"]))

    # Convert journals set to list of dicts
    for drug, refs in mapping.items():
        refs["journals"] = [
            {"journal": journal, "date": date} for journal, date in refs["journals"]
        ]

    return mapping
