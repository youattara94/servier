import logging

from drug_publication_pipeline.data_export import write_json_file
from drug_publication_pipeline.data_loader import read_file
from drug_publication_pipeline.data_processor import (
    find_drug_references,
    map_drugs_to_publications,
)


class Pipeline:
    def __init__(self, input_file_paths: dict[str, str], output_file_path: str):
        self.input_file_paths = input_file_paths
        self.output_file_path = output_file_path

    def run(self) -> None:
        """
        Executes the pipeline by reading input files, processing data, and writing to the output file.
        """

        logging.info("Starting the drug publication pipeline...")

        # Load input data
        logging.info("Loading input data from files...")
        drugs_df = read_file(self.input_file_paths["drugs"])
        clinical_trials_df = read_file(self.input_file_paths["clinical_trials"])
        pubmed_csv_df = read_file(self.input_file_paths["pubmed_csv"])
        pubmed_json_df = read_file(self.input_file_paths["pubmed_json"])

        # Find drug references among the input files
        logging.info("Finding drug references in publications...")
        pubmed_csv_refs = find_drug_references(drugs_df, pubmed_csv_df, "title")
        pubmed_json_refs = find_drug_references(drugs_df, pubmed_json_df, "title")
        clinical_trials_refs = find_drug_references(
            drugs_df, clinical_trials_df, "scientific_title"
        )

        # Combine all PubMed references
        all_pubmed_refs = pubmed_csv_refs + pubmed_json_refs

        # Create mapping between drugs and publications in which there are referenced
        logging.info("Mapping drugs to their publication references...")
        drug_publication_mapping = map_drugs_to_publications(
            drugs_df, all_pubmed_refs, clinical_trials_refs
        )

        # Save the mapping to the output JSON file
        logging.info("Writing drug publication mapping to output file...")
        write_json_file(drug_publication_mapping, self.output_file_path)
        logging.info(f"Output written to {self.output_file_path}")

        logging.info("Pipeline execution completed successfully.")
