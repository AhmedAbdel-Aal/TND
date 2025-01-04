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
