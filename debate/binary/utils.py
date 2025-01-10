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


def format_prompt(template: str, **kwargs) -> str:
    """Format a prompt template with variables."""
    try:
        return template.format(**kwargs)
    except KeyError as e:
        raise ValueError(f"Missing required prompt variable: {e}")


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
        r"ANALYSIS:\s*(.*?)(?=(CLASSIFICATION:|REASONING:|$))", text, re.S
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


def construct_other_agents_answer(agents, current_agent):
    prefix_string = "These are the recent/updated opinions from other legal agents: "
    postfix_string = """
Please provide an updated answer based on the reasoning of the other agents.
Examine your solution and the other agents' step-by-step
If you decided to keep your original classification, please provide a justification and argue against the other agents' reasoning.
If you decided to change your classification, please provide a justification and explain why the other agents' reasoning is flawed.

## Output Format:
Return your response in this format:
ANALYSIS: [Your space present your updated analysis and argumentation]
CLASSIFICATION: [KEY CASE, NOT KEY CASE]
REASONING: [The reasons behind your classification]
"""

    for agent in agents:
        if agent.name != current_agent.name:
            agent_response = agent.get_latest_response()
            response = "\n\n One agent response: ```{}```".format(agent_response)
            prefix_string = prefix_string + response

    prefix_string = prefix_string + postfix_string
    return prefix_string
