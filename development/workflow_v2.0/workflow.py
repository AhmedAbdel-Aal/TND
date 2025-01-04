import pandas as pd
import os
import time
import dotenv
from tqdm import tqdm

from steps import do_stage_1, do_stage_2, do_stage_3, get_probabilities

from citation_analyzer.citation_extractor import analyze_citations


from utils import save_json, load_json

dotenv.load_dotenv()

input_data_root = "/Users/ahmed/Desktop/msc-24/ECHR/echr-processed"
output_dir = "/Users/ahmed/Desktop/msc-24/TND/workflow_v2.0/results_logs"


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

    return list_1[4:], list_2[:1], list_3[:1], list_4[:1]


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
            facts = case_data["facts"]
            law = case_data["law"]
            case_name = case_data["docname"]
            articles = case_data["__articles"]

            # Run the workflow
            print("Citation Analysis: ...")
            citation_analysis = analyze_citations(file_path)
            # print('Running stages 1, 2, 3 ...')
            # stage_1 = do_stage_1(articles)
            # stage_2 = do_stage_2(case_name, facts, law, stage_1)
            # stage_3 = do_stage_3(case_name, facts, law, citation_analysis, stage_1, stage_2)
            # print('Calculating probabilities ...')
            # probabilities = get_probabilities(case_name, facts, law, citation_analysis, stage_1, stage_2, stage_3)

            # Aggregate results and classify case importance
            results = {
                "citation_analysis": citation_analysis,
                # "stage_1": stage_1,
                # "stage_2": stage_2,
                # "stage_3": stage_3,
                #'probabilities': probabilities
            }

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
    # print("Running workflow for list 2")
    # run_workflow(list_2)
    # print("Running workflow for list 3")
    # run_workflow(list_3)
    # print("Running workflow for list 4")
    # run_workflow(list_4)


if __name__ == "__main__":
    main()
