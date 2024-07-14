import torch
import torch.nn as nn
from torch.cuda.amp import autocast, GradScaler
from sklearn.metrics import f1_score, accuracy_score
import wandb
from tqdm import tqdm

def evaluate(model, dataloader, device):
    model.eval()
    val_loss = 0.0
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for batch in tqdm(dataloader, desc="Validation"):
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            with autocast():
                outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                loss = nn.CrossEntropyLoss()(outputs, labels)
                val_loss += loss.item()

                preds = torch.argmax(outputs, dim=1)
                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())

    avg_val_loss = val_loss / len(dataloader)
    f1 = f1_score(all_labels, all_preds, average='weighted')
    micro_f1 = f1_score(all_labels, all_preds, average='micro')
    macro_f1 = f1_score(all_labels, all_preds, average='macro')
    accuracy = accuracy_score(all_labels, all_preds)

    return avg_val_loss, f1, micro_f1, macro_f1, accuracy