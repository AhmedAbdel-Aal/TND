import pandas as pd
import os
from utils import get_df_metrics, get_heatmap, load_json


# get the results dir from user
import argparse

parser = argparse.ArgumentParser(description="Get the results dir")
parser.add_argument(
    "--results_dir", type=str, help="The directory containing the results"
)
args = parser.parse_args()
results_dir = args.results_dir

## example usage
# example 1: python calc_metrics.py --results_dir ./results_openai_gpt4-mini/
# example 2: python calc_metrics.py --results_dir ./results_openai_gpt4-mini/
# example 3: python calc_metrics.py --results_dir ./results_openai_gpt4-mini/
# example 4: python calc_metrics.py --results_dir ./results_openai_gpt4-mini/


def return_binary_classification(result):
    if "NOT KEY CASE" in result:
        return 0
    else:
        return 1


def transalte_importance_score(importance):
    if importance == "1":
        return 1
    else:
        return 0


def get_metrics(mode="all"):
    results = os.listdir(results_dir)
    results = [r for r in results if r.endswith(".json")]
    filtered_results = []
    if mode == "all":
        filtered_results = results
    elif mode == "1_2":
        filtered_results = [r for r in results if "i_1" in r or "i_2" in r]
    elif mode == "1_3":
        filtered_results = [r for r in results if "i_1" in r or "i_3" in r]
    elif mode == "1_4":
        filtered_results = [r for r in results if "i_1" in r or "i_4" in r]
    else:
        raise ValueError("mode should be either all, 1_2, 1_3, 1_4")

    data = []
    for result in filtered_results:
        result_data = load_json(os.path.join(results_dir, result))
        data.append(
            {
                #'id': result_data['id'],
                "classification": return_binary_classification(
                    result_data["result"]["output"]
                ),
                "ground_truth": transalte_importance_score(result_data["importance"]),
            }
        )

    df = pd.DataFrame(data)

    metrics_dict = get_df_metrics(df, "classification", "ground_truth")
    print(metrics_dict)
    get_heatmap(df, "classification", "ground_truth")


if __name__ == "__main__":
    print("All")
    get_metrics("all")

    # print('1_2')
    # get_metrics("1_2")

    # print('1_3')
    # get_metrics('1_3')

    # print('1_4')
    # get_metrics('1_4')
