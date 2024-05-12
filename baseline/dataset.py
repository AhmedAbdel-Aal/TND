import os
import torch
import json
from torch.utils.data import Dataset
from torch.nn.utils.rnn import pad_sequence
from transformers import LongformerTokenizerFast

class ECHRDataset(Dataset):
    def __init__(self, data_path, tokenizer_name = "allenai/longformer-base-4096" , max_length=512):
        self.data_path = data_path
        self.tokenizer = LongformerTokenizerFast.from_pretrained(tokenizer_name)
        self.max_length = max_length
        self.data = []

        print(f"Using Tokenizer {tokenizer_name} with max_length {self.max_length}")

        # Load and preprocess the data
        self.load_and_preprocess()

    def load_and_preprocess(self):
        files = [f for f in os.listdir(self.data_path) if f.endswith('.json')]
        for file in files:
            path = os.path.join(self.data_path, file)
            with open(path, 'r', encoding='utf-8') as f:
                document = json.load(f)
                text = document.get('facts', '')
                label = document.get('importance', '')
                self.data.append({'facts': text, 'importance': label})

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        text = item['facts']
        label = int(item['importance'])
        encoded = self.tokenizer(text, truncation=True, padding='max_length', max_length=self.max_length)
        return {
            'input_ids': encoded['input_ids'],
            'attention_mask': encoded['attention_mask'],
            'label': torch.tensor(label, dtype=torch.float)
        }

    def collate_fn(self, batch):
        input_ids = pad_sequence(
            [torch.tensor(item['input_ids'], dtype=torch.long) for item in batch],
            batch_first=True
        )
        attention_mask = pad_sequence(
            [torch.tensor(item['attention_mask'], dtype=torch.long) for item in batch],
            batch_first=True
        )
        labels = torch.stack([item['label'] for item in batch])
        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': labels
        }