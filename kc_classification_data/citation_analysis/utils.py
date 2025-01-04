import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix


def load_json(file_path: str):
    """Load and return data from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def save_json(file_path: str, data: any):
    """Save data to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_txt(file_path: str):
    """Load and return contents of a text file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()
    return data


def save_txt(file_path: str, data: str):
    """Save data to a text file."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data)


def from_input_path_to_output_path(file_path: str):
    """Convert an input file path to an output file path."""
    case = load_json(file_path)
    prefix = case["importance"]
    itemid = case["itemid"]
    output_file_name = f"i_{prefix}_case_{itemid}.json"
    output_file_path = (
        "/Users/ahmed/Desktop/msc-24/TND/key_case_binary_classification/pre_cutoff_analysis/react_1/results_openai_gpt4-mini/"
        + output_file_name
    )
    return output_file_path


def get_df_metrics(df: pd.DataFrame, target_col: str, pred_col: str):
    """Calculate and return classification metrics for a DataFrame."""
    from sklearn.metrics import classification_report

    y_true = df[target_col]
    y_pred = df[pred_col]

    # calculate accuracy
    accuracy = (df["classification"] == df["ground_truth"]).sum() / len(df)

    # calculate precision
    precision = (df["classification"] & df["ground_truth"]).sum() / df[
        "classification"
    ].sum()

    # calculate recall
    recall = (df["classification"] & df["ground_truth"]).sum() / df[
        "ground_truth"
    ].sum()

    # calculate f1 score
    f1 = 2 * (precision * recall) / (precision + recall)

    metrics = {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1}
    return metrics


def get_heatmap(df: pd.DataFrame, target_col: str, pred_col: str):
    """Plot and display a heatmap of the confusion matrix."""

    cm = confusion_matrix(df[target_col], df[pred_col])
    sns.heatmap(cm, annot=True, fmt="g", cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.show()


import difflib
import string
import re
from unidecode import unidecode


def normalize(s):
    # Example: uppercase, remove punctuation, remove extra spaces
    # remove accents:
    s = unidecode(s)
    s = s.upper()
    s = s.translate(str.maketrans("", "", string.punctuation))  # remove punctuation
    s = " ".join(s.split())  # remove extra spaces
    return s


def find_closest_match(target_name, cases_names):
    # Store the matches in a set to remove duplicates
    matches = set()

    # First, find all matches based on substrings
    for name in cases_names:
        if name in target_name:
            matches.add(name)
        if target_name in name:
            matches.add(name)

    # If there are no matches, return None or empty list
    if not matches:
        return None

    # If there is only one match, return it directly
    if len(matches) == 1:
        return next(iter(matches))

    # If there's more than one match, find the closest one using fuzzy matching
    closest_match = None
    highest_similarity = 0

    for match in matches:
        similarity = difflib.SequenceMatcher(None, target_name, match).ratio()
        if similarity > highest_similarity:
            highest_similarity = similarity
            closest_match = match

    return closest_match
