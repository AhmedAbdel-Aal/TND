import dotenv
import os
import time
from tqdm import tqdm
import pandas as pd
from utils import load_json, save_json, text_to_json
import logging

from cot import cot_facts, cot_law, cot_facts_law

dotenv.load_dotenv()

# diabsle deprecation warning
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

## configs
input_data_root = "/Users/ahmed/Desktop/msc-24/ECHR/echr-processed"
output_dir = "./results_deepseek/"


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


def infere(paths_list):
    already_processed_files = os.listdir(output_dir)

    # remove the prefix kc_ and not_kc_
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

    for file_path in tqdm(paths_list):
        # read the case file
        if file_path in already_processed_files:
            continue
        case_path = os.path.join(input_data_root, file_path)
        case_data = load_json(case_path)
        case_facts = case_data["facts"]
        case_law = case_data["law"]

        # classify the case
        cot_facts_response = cot_facts(case_facts)
        cot_law_response = cot_law(case_law)
        cot_facts_law_response = cot_facts_law(case_facts, case_law)

        try:
            cot_facts_response = text_to_json(cot_facts_response)
            cot_law_response = text_to_json(cot_law_response)
            cot_facts_law_response = text_to_json(cot_facts_law_response)
        except:
            print(f"Error in case: {file_path}")
            continue

        # write the result to a file
        output_result = {}
        output_result["cot_facts"] = cot_facts_response
        output_result["cot_law"] = cot_law_response
        output_result["cot_facts_law"] = cot_facts_law_response
        output_result["importance"] = case_data["importance"]

        save_json(
            output_dir + f'i_{case_data["importance"]}_case_{file_path}', output_result
        )
        # time.sleep(3)


def main():
    list_1, list_2, list_3, list_4 = read_data()
    print(f"Number of cases in list 1: {len(list_1)}")
    infere(list_1)
    print(f"Number of cases in list 2: {len(list_2)}")
    infere(list_2)
    print(f"Number of cases in list 3: {len(list_3)}")
    infere(list_3)
    print(f"Number of cases in list 4: {len(list_4)}")
    infere(list_4)


if __name__ == "__main__":
    main()
