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


def extract_paragraphs_from_list(text_lines, start_para, end_para):
    """
    Extract paragraphs between start and end paragraph numbers.
    Handles unnumbered paragraphs by including them until finding a number larger than end_para.
    """
    paragraphs = []
    current_paragraph = ""
    is_collecting = False

    # Clean and normalize text lines
    clean_lines = [line.strip().strip('"') for line in text_lines if line.strip()]

    for line in clean_lines:
        # Try to extract paragraph number if present
        current_number = None
        if line.split(".")[0].strip().isdigit():
            current_number = int(line.split(".")[0].strip())

        # Start collecting when we hit start_para
        if current_number == start_para:
            is_collecting = True
            current_paragraph = line
            continue

        # Stop collecting when we hit a number larger than end_para
        if current_number is not None and current_number > end_para:
            if current_paragraph:
                paragraphs.append(current_paragraph)
            break

        # If we're collecting, handle the current line
        if is_collecting:
            # If it's a new numbered paragraph within our range
            if current_number is not None and start_para <= current_number <= end_para:
                if current_paragraph:
                    paragraphs.append(current_paragraph)
                current_paragraph = line
            else:
                # It's a continuation of the current paragraph
                current_paragraph += " " + line

    # Add the last paragraph if we have one
    if is_collecting and current_paragraph:
        paragraphs.append(current_paragraph)

    # to string
    paragraphs = "\n".join(paragraphs)

    return paragraphs


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


from openai import OpenAI


def llm_call(prompt):

    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return completion.choices[0].message.content
