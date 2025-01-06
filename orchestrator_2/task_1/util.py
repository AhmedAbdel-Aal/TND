from openai import OpenAI
import os
import re
import json
import dotenv

dotenv.load_dotenv()


def llm_call_deepseek(prompt):

    client = OpenAI(
        api_key=os.environ["DEEP_SEEK"], base_url="https://api.deepseek.com"
    )
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.",
            },
            {"role": "user", "content": prompt},
        ],
        stream=False,
    )
    return response.choices[0].message.content


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


def llm_call(prompt, beackend, model="gpt-4o-mini"):
    if beackend == "openai":
        return llm_call_openai(prompt, model)
    elif beackend == "deepseek":
        return llm_call_deepseek(prompt)
    else:
        raise ValueError("Invalid backend")


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
