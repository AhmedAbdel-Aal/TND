import os
import torch
import json
from torch.utils.data import Dataset
from transformers import AutoModel, AutoTokenizer


# load txt file into a list
def load_files(path):
    with open(path) as f:
        train_files = f.readlines()
        train_files = [x.strip() for x in train_files]
    return train_files

def map_label_to_int(label):
    'maps the labels to the classes key case, not key case'
    label = int(label)
    if label in [1]:
        return 1
    elif label in [2,3,4]:
        return 0


class ECHRDataset(Dataset):
    def __init__(
        self, train_files_path, data_path, tokenizer, max_length=8192
    ):
        self.data_path = data_path
        self.train_files_path = train_files_path
        self.max_length = max_length
        self.tokenizer = tokenizer # AutoTokenizer.from_pretrained(tokenizer_name)
        self.data = []

        print(f"Using Tokenizer {tokenizer.name_or_path}")

        # Load and preprocess the data
        self.load_and_preprocess()

    def load_and_preprocess(self):
        files = load_files(self.train_files_path)
        for file in files:
            path = os.path.join(self.data_path, file)
            with open(path, "r", encoding="utf-8") as f:
                document = json.load(f)
                itemid = document.get("itemid", "")
                text = document.get('facts', '')
                label = document.get("importance", "")
                self.data.append({"itemid": itemid, "text": text, "importance": label})

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        text = item["text"]
        label = map_label_to_int(item["importance"])
        encoded = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt"
        )

        return {
            "input_ids": encoded["input_ids"].squeeze(0),
            "attention_mask": encoded["attention_mask"].squeeze(0),
            "label": torch.tensor(label),
            "itemid": item["itemid"]
        }