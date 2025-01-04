import dotenv
import os
import time
from tqdm import tqdm
import pandas as pd
from legal_case_classifier import LegalCaseClassifier
from utils import load_json, save_json
import logging

dotenv.load_dotenv()

# diabsle deprecation warning
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

## configs
input_data_root = "../../../../ECHR/echr-processed/"
output_dir = "./results_facts_gptsmp2/"
prompt_id = "4"
backend = "openai"
input_sections = ["facts"]


def read_data():
    df_1 = pd.read_csv("../../../kc_classification_data/pre_cutoff_data/df_1.csv")
    list_1 = df_1["file_path"].to_list()

    df_2 = pd.read_csv("../../../kc_classification_data/pre_cutoff_data/df_2.csv")
    list_2 = df_2["file_path"].to_list()

    df_3 = pd.read_csv("../../../kc_classification_data/pre_cutoff_data/df_3.csv")
    list_3 = df_3["file_path"].to_list()

    df_4 = pd.read_csv("../../../kc_classification_data/pre_cutoff_data/df_4.csv")
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

    for file_path in tqdm(paths_list[:25]):
        # read the case file
        if file_path in already_processed_files:
            continue
        case_path = os.path.join(input_data_root, file_path)
        case_data = load_json(case_path)
        case_facts = case_data["facts"]

        # classify the case
        classifier = LegalCaseClassifier(prompt_id=prompt_id, backend=backend)
        if input_sections == ["facts", "law"]:
            result = classifier.classify_case(
                case_facts=case_facts, law=case_data["law"]
            )
        elif input_sections == ["facts"]:
            result = classifier.classify_case(case_facts=case_facts)
        else:
            raise ValueError(
                'input_sections should be either ["facts", "law"] or ["facts"]'
            )

        # write the result to a file
        output_result = {}
        output_result["result"] = result
        output_result["importance"] = case_data["importance"]
        output_result["date"] = case_data["judgementdate"]

        save_json(
            output_dir + f'i_{case_data["importance"]}_case_{file_path}', output_result
        )
        time.sleep(5)


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
