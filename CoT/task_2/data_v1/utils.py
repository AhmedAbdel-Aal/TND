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


import re


def text_to_json(text):
    """
    Transform a formatted text string into a JSON object.
    The text should contain sections marked with EXPLANATION:, CLASSIFICATION:, and REASONING:

    Args:
        text (str): The input text to transform

    Returns:
        dict: A dictionary containing the parsed sections
    """
    # Regex to match each section
    explanation_match = re.search(
        r"EXPLANATION:\s*(.*?)(?=(CLASSIFICATION:|REASONING:|$))", text, re.S
    )
    classification_match = re.search(
        r"CLASSIFICATION:\s*(.*?)(?=(EXPLANATION:|REASONING:|$))", text, re.S
    )
    reasoning_match = re.search(
        r"REASONING:\s*(.*?)(?=(EXPLANATION:|CLASSIFICATION:|$))", text, re.S
    )

    # Extract the content for each section if it exists
    result = {
        "explanation": explanation_match.group(1).strip() if explanation_match else "",
        "classification": (
            classification_match.group(1).strip() if classification_match else ""
        ),
        "reasoning": reasoning_match.group(1).strip() if reasoning_match else "",
    }

    return result
