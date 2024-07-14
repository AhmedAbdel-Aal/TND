import torch
from torch import nn
from transformers import LongformerModel, LongformerConfig

class ECHRModel(nn.Module):
    def __init__(self, model_name='allenai/longformer-base-4096', num_labels=4):
        super(ECHRModel, self).__init__()
        self.config = LongformerConfig.from_pretrained(model_name)
        self.longformer = LongformerModel.from_pretrained(model_name, config=self.config)
        self.classifier = nn.Linear(self.config.hidden_size, num_labels)

    def forward(self, input_ids, attention_mask):
        outputs = self.longformer(input_ids=input_ids, attention_mask=attention_mask)
        # Take the hidden state of the [CLS] token (first token)
        cls_output = outputs[0][:, 0, :]
        logits = self.classifier(cls_output)
        return logits
