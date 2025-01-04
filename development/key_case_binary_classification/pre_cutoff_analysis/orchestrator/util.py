from anthropic import Anthropic
from openai import OpenAI
import os
import re
import json

import dotenv

dotenv.load_dotenv()


def llm_call_anthropic(prompt: str, model="claude-3-5-sonnet-20241022") -> str:
    """
    Calls the model with the given prompt and returns the response.

    Args:
        prompt (str): The user prompt to send to the model.
        system_prompt (str, optional): The system prompt to send to the model. Defaults to "".
        model (str, optional): The model to use for the call. Defaults to "claude-3-5-sonnet-20241022".

    Returns:
        str: The response from the language model.
    """
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    messages = [{"role": "user", "content": prompt}]
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system="You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.",
        messages=messages,
        temperature=0.1,
    )
    return response.content[0].text


def llm_call_openai(prompt, model="gpt-4o-mini"):

    client = OpenAI()
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return completion.choices[0].message.content


def llm_call(prompt, backend="openai"):
    if backend == "anthropic":
        return llm_call_anthropic(prompt)
    elif backend == "openai":
        return llm_call_openai(prompt)
    else:
        raise ValueError(f"Invalid backend: {backend}")


def extract_xml(text: str, tag: str) -> str:
    """
    Extracts the content of the specified XML tag from the given text. Used for parsing structured responses

    Args:
        text (str): The text containing the XML.
        tag (str): The XML tag to extract content from.

    Returns:
        str: The content of the specified XML tag, or an empty string if the tag is not found.
    """
    match = re.search(f"<{tag}>(.*?)</{tag}>", text, re.DOTALL)
    return match.group(1) if match else ""


def load_json(file_path: str):
    """Load and return data from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def save_json(file_path: str, data: any):
    """Save data to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


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
