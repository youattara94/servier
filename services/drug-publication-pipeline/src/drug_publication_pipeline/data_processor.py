import pandas as pd


def find_drug_references(
    drugs_df: pd.DataFrame, publications_df: pd.DataFrame, column_name: str
) -> list[dict[str, str]]:
    """Finds references to drugs in a given column of publications DataFrame"""
    references = []
    for _, drug in drugs_df.iterrows():
        drug_name = drug["drug"].lower()
        for _, pub in publications_df.iterrows():
            if drug_name in pub[column_name].lower():
                references.append(
                    {
                        "drug": drug["drug"],
                        "title": pub[column_name],
                        "journal": pub["journal"],
                        "date": pub["date"],
                    }
                )
    return references


def map_drugs_to_publications(
    drugs_df: pd.DataFrame,
    pubmed_references: list[dict[str, str]],
    clinical_trials_references: list[dict[str, str]],
) -> dict[str, dict[str, list[dict[str, str]]]]:
    """
    Maps drugs to their references in PubMed and clinical trials, including journal information
    """
    mapping = {}

    # Initialize mapping structure
    for _, drug in drugs_df.iterrows():
        drug_name = drug["drug"]
        mapping[drug_name] = {
            "pubmed_references": [],
            "clinical_trials_references": [],
            "journals": set(),
        }

    # Add PubMed references
    for ref in pubmed_references:
        drug = ref["drug"]
        mapping[drug]["pubmed_references"].append(
            {"title": ref["title"], "date": ref["date"]}
        )
        mapping[drug]["journals"].add((ref["journal"], ref["date"]))

    # Add clinical trials references
    for ref in clinical_trials_references:
        drug = ref["drug"]
        mapping[drug]["clinical_trials_references"].append(
            {"title": ref["title"], "date": ref["date"]}
        )
        mapping[drug]["journals"].add((ref["journal"], ref["date"]))

    # Convert journals set to list of dicts
    for drug, refs in mapping.items():
        refs["journals"] = [
            {"journal": journal, "date": date} for journal, date in refs["journals"]
        ]

    return mapping
