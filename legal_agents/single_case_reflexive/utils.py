import os
from transformers import AutoTokenizer
from nltk import tokenize


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
