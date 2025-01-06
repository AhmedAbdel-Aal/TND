import pandas as pd
import os
import time
import dotenv
from tqdm import tqdm

from prompts import CLAIM_DECOMPOSER_PROMPT, A, B, C1, C2, D1
from orchestrator import FlexibleOrchestrator

from util import load_json, save_json

dotenv.load_dotenv()

input_data_root = "/Users/ahmed/Desktop/msc-24/ECHR/echr-processed"
output_dir = "/Users/ahmed/Desktop/msc-24/TND/orchestrator_2/task_1/results"


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

    return list_1[:3], list_2[:3], list_3[:3], list_4[:3]


def translate_importance(importance):
    if importance == 1:
        return "Key Case"
    elif importance == 2:
        return "High importance - not key case"
    elif importance == 3:
        return "medium importance - not key case"
    elif importance == 4:
        return "low importance - not key case"
    else:
        return "unknown"


def load_key_case_one_liner(itemid):
    one_liners = load_json(
        "/Users/ahmed/Desktop/msc-24/TND/kc_classification_data/key_cases_lines/key_cases_lines.json"
    )
    return one_liners[itemid]


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
        case_facts = case_data["facts"]
        case_law = case_data["law"]
        importance = int(case_data["importance"])
        importance_translated = translate_importance(importance)
        one_liner = "None"
        if importance == 1:
            one_liner = load_key_case_one_liner(case_data["itemid"])

        orchestrator = FlexibleOrchestrator(
            claim_decomposer_prompt=CLAIM_DECOMPOSER_PROMPT,
            prompt_a=A,
            prompt_b=B,
            prompt_c1=C1,
            prompt_c2=C2,
            prompt_d1=D1,
            case_facts=case_facts,
            case_law=case_law,
        )

        list_of_responses = orchestrator.process()

        # add metadata
        results = {}
        results["responses"] = list_of_responses
        results["importance"] = importance
        results["importance_translated"] = importance_translated
        results["itemid"] = case_data["itemid"]
        results["one_liner"] = one_liner

        output_file_name = f'i_{case_data["importance"]}_case_{file_path}'
        save_json(os.path.join(output_dir, output_file_name), results)

        time.sleep(3)


def main():
    list_1, list_2, list_3, list_4 = read_data()
    print("Running workflow for list 1")
    run_workflow(list_1)
    print("Running workflow for list 2")
    # run_workflow(list_2)
    print("Running workflow for list 3")
    # run_workflow(list_3)
    print("Running workflow for list 4")
    run_workflow(list_4)


if __name__ == "__main__":
    main()
