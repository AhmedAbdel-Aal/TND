import pandas as pd
import os
import time
import dotenv
from tqdm import tqdm

from llm import (
    summarize_facts,
    summarize_law,
    extract_legal_principles,
    perform_citation_analysis,
)
from llm import classify_key_case_importance_workflow_4
from llm import classify_three_levels_importance_workflow_4
from llm import classify_four_levels_importance_workflow_4

from utils import save_json, load_json

dotenv.load_dotenv()

input_data_root = "/Users/ahmed/Desktop/msc-24/ECHR/echr-processed"
output_dir = "/Users/ahmed/Desktop/msc-24/TND/workflow_parallelization/results_workflow_4_facts_law"


def read_data():
    df_1 = pd.read_csv(
        "/Users/ahmed/Desktop/msc-24/TND/kc_classification_data/pre_cutoff_data/df_1.csv"
    )
    list_1 = df_1["file_path"].to_list()

    df_2 = pd.read_csv(
        "/Users/ahmed/Desktop/msc-24/TND/kc_classification_data/pre_cutoff_data/df_2.csv"
    )
    list_2 = df_2["file_path"].to_list()

    df_3 = pd.read_csv(
        "/Users/ahmed/Desktop/msc-24/TND/kc_classification_data/pre_cutoff_data/df_3.csv"
    )
    list_3 = df_3["file_path"].to_list()

    df_4 = pd.read_csv(
        "/Users/ahmed/Desktop/msc-24/TND/kc_classification_data/pre_cutoff_data/df_4.csv"
    )
    list_4 = df_4["file_path"].to_list()

    return list_1, list_2, list_3, list_4


def check_processed_files():
    already_processed_files = os.listdir(output_dir)

    # remove the prefix
    already_processed_files = [
        f.replace("i_1_case_", "") for f in already_processed_files
    ]
    already_processed_files = [
        f.replace("i_2_case_", "") for f in already_processed_files
    ]
    already_processed_files = [
        f.replace("i_3_case_", "") for f in already_processed_files
    ]
    already_processed_files = [
        f.replace("i_4_case_", "") for f in already_processed_files
    ]
    return already_processed_files


def run_workflow(list):
    already_processed_files = check_processed_files()

    for file_path in tqdm(list):
        # skip already processed files
        if file_path in already_processed_files:
            continue

        # read the case file
        print(f"Processing file: {file_path}")
        case_path = os.path.join(input_data_root, file_path)
        case_data = load_json(case_path)
        law = case_data["law"]

        # Run the workflow
        print("Load facts.")
        facts = case_data["facts"]
        print("Load law.")
        law = case_data["law"]
        print("Extracting legal principles.")
        legal_principles = extract_legal_principles(facts, file_path=file_path)
        print("Performing citation analysis.")
        citation_analysis = perform_citation_analysis(facts, law, file_path=file_path)

        # Aggregate results and classify case importance
        inputs = {
            "facts_summary": facts,
            "law_summary": law,
            "legal_principles": legal_principles,
            "citation_analysis": citation_analysis,
        }

        # classify case importance
        print("Classifying case importance.")
        key_case_importance = classify_key_case_importance_workflow_4(inputs)
        three_levels_importance = classify_three_levels_importance_workflow_4(inputs)
        four_levels_importance = classify_four_levels_importance_workflow_4(inputs)

        # save the results
        results = {
            "steps": {
                "summarize_facts": facts,
                "summarize_law": law,
                "extract_legal_principles": legal_principles,
                "citation_analysis": citation_analysis,
            },
            "key_case_importance": key_case_importance,
            "three_levels_importance": three_levels_importance,
            "four_levels_importance": four_levels_importance,
            "ground_truth": case_data["importance"],
        }
        output_file_name = f'i_{case_data["importance"]}_case_{file_path}'
        save_json(os.path.join(output_dir, output_file_name), results)

        time.sleep(3)


def main():
    list_1, list_2, list_3, list_4 = read_data()
    print("Running workflow for list 2")
    run_workflow(list_2)
    print("Running workflow for list 3")
    run_workflow(list_3)
    print("Running workflow for list 1")
    run_workflow(list_1)
    print("Running workflow for list 4")
    run_workflow(list_4)


if __name__ == "__main__":
    main()
