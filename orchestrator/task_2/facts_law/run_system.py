import pandas as pd
import os
import time
import dotenv
from tqdm import tqdm

from prompts import ORCHESTRATOR_PROMPT, SYNTHESIZER_PROMPT, WORKER_PROMPT
from orchestrator import FlexibleOrchestrator

from util import load_json, save_json

dotenv.load_dotenv()

input_data_root = "/Users/ahmed/Desktop/msc-24/ECHR/echr-processed"
output_dir = "/Users/ahmed/Desktop/msc-24/TND/key_case_binary_classification/pre_cutoff_analysis/orchestrator/results_facts"


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
        try:
            # read the case file
            print(f"Processing file: {file_path}")
            case_path = os.path.join(input_data_root, file_path)
            case_data = load_json(case_path)
            case_facts = case_data["facts"]
            # case_law = case_data['law']

            orchestrator = FlexibleOrchestrator(
                orchestrator_prompt=ORCHESTRATOR_PROMPT,
                synthetizer_prompt=SYNTHESIZER_PROMPT,
                worker_prompt=WORKER_PROMPT,
                case_facts=case_facts,
                # case_law=case_law
            )

            results = orchestrator.process(
                task=f"""
You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.
Your task is to analyze the provided case facts and classify the case into one of the following categories:

KEY CASE:
- Makes a significant contribution to the development, clarification, or modification of case law.
- Establishes new legal principles or substantially modifies existing ones.
- Has broad implications beyond the immediate case.

NOT KEY CASE:
- Applies existing case law without significant contributions to legal development.
- Demonstrates limited implications beyond the immediate dispute.

<Facts>
{case_facts}.
</Facts>

Based on the facts and law provided, classify the case as either a Key Case or a Non-Key Case. Your decision should be based strictly on the criteria above.
            """
            )

            output_file_name = f'i_{case_data["importance"]}_case_{file_path}'
            save_json(os.path.join(output_dir, output_file_name), results)

            time.sleep(3)
        except Exception as e:
            print(f"Error processing file: {file_path}")
            print(e)
            continue


def main():
    list_1, list_2, list_3, list_4 = read_data()
    print("Running workflow for list 1")
    run_workflow(list_1)
    print("Running workflow for list 2")
    run_workflow(list_2)
    print("Running workflow for list 3")
    run_workflow(list_3)
    print("Running workflow for list 4")
    run_workflow(list_4)


if __name__ == "__main__":
    main()
