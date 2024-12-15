import os
import json
from transformers import AutoTokenizer
from nltk import tokenize


def load_json(path):
    with open(path, "r") as f:
        data = json.load(f)
    return data


def load_txt(path):
    with open(path, "r") as f:
        data = f.read()
    return data


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def count_tokens(text):
    # if 'llama' in self.model_name:
    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    tokens = tokenizer.tokenize(text)
    num_tokens = len(tokens)
    return num_tokens


def get_sentences(text):
    sentences = tokenize.sent_tokenize(text)
    merged_sentences = []

    sentence = ""
    for idx, i in enumerate(sentences):
        sentence += i
        if len(i) < 10:
            continue
        else:
            merged_sentences.append(sentence)
            sentence = ""

    return merged_sentences


def overlapping_split(text, token_limit=7500, overlap=300):
    words = len(text.split(" "))
    num_tokens = count_tokens(text)
    sentences = get_sentences(text)
    print(
        f"text has {words} words and {len(sentences)} sentences, on average {words/len(sentences)} word/sentecesand {num_tokens} tokens, token limit is {token_limit}"
    )

    if num_tokens <= token_limit:
        return text

    chuncks = (num_tokens // token_limit) + 1 + 1
    sentences_in_chunck = (len(sentences) // chuncks) - 10
    spliited_sentences = [
        sentences[i : i + sentences_in_chunck]
        for i in range(0, len(sentences), sentences_in_chunck)
    ]
    return spliited_sentences


import re


def get_last_question(text):
    # Regex pattern to match questions, considering multiline questions
    pattern = r"(Question:\s*.*?)(?=\n[A-Z]|\Z)"

    # Find all matches with the multiline flag enabled
    matches = re.findall(pattern, text, re.DOTALL)

    # Get the last match
    last_question = matches[-1] if matches else None

    return last_question


def check_for_stop(text):
    # Regex pattern to match questions, considering multiline questions
    pattern = r"(Stop:\s*.*?)(?=\n[A-Z]|\Z)"

    # Find all matches with the multiline flag enabled
    matches = re.findall(pattern, text, re.DOTALL)

    # Get the last match
    stop = matches[-1] if matches else None

    return stop


def check_for_final_answer(text):
    # Regex pattern to match questions, considering multiline questions
    pattern = r"(Final Answer:\s*.*?)(?=\n[A-Z]|\Z)"

    # Find all matches with the multiline flag enabled
    matches = re.findall(pattern, text, re.DOTALL)

    # Get the last match
    stop = matches[-1] if matches else None

    return stop


def save_txt_file(file_name, content):
    with open(file_name, "w") as f:
        f.write(content)
