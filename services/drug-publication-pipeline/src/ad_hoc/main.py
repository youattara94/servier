import json
import logging
from collections import defaultdict

from drug_publication_pipeline.settings import settings

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():
    """
    Main function to find the journal that mentions the most different drugs.
    """
    with open(settings().output_json_file, "r", encoding="utf-8") as f:
        output_data = json.load(f)

    # Dictionary to store drugs by journal
    journal_to_drugs = defaultdict(set)

    for drug, info in output_data.items():
        for journal_entry in info["journals"]:
            journal_name = journal_entry["journal"]
            journal_to_drugs[journal_name].add(drug)

    # For each journal, count the number of unique drugs mentioned
    max_count = 0
    top_journal = None

    for journal, drugs in journal_to_drugs.items():
        count = len(drugs)
        if count > max_count:
            max_count = count
            top_journal = journal
        elif count == max_count:
            # When there's a tie, we keep the first found
            pass

    logging.info(f"Top journal: {top_journal} with {max_count} unique drugs mentioned")


if __name__ == "__main__":
    main()
