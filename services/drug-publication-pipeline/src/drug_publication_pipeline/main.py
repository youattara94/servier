import logging

from drug_publication_pipeline.pipeline import Pipeline

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main() -> None:
    """
    Main function to run the drug publication pipeline.
    Reads input files, processes data, and writes to the output file.
    """
    input_file_paths = {
        "drugs": "input/drugs.csv",
        "clinical_trials": "input/clinical_trials.csv",
        "pubmed_csv": "input/pubmed.csv",
        "pubmed_json": "input/pubmed.json",
    }
    output_file_path = "output/drug_publication_references.json"

    pipeline = Pipeline(input_file_paths, output_file_path)
    pipeline.run()


if __name__ == "__main__":
    main()
