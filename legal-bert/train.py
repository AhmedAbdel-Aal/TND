import torch
import wandb
import numpy as np
from sklearn.metrics import f1_score

from transformers import LongformerTokenizerFast, LongformerForSequenceClassification, Trainer, TrainingArguments, LongformerConfig
from transformers import LongformerModel, LongformerTokenizer
from transformers import DataCollatorWithPadding, LongformerForSequenceClassification
from transformers import TrainerCallback

from data import ECHRDataset

# start a new wandb run to track this script
wandb.init(
    # set the wandb project where this run will be logged
    project="longformer-4096-facts-3-classes",
)

def set_seed(seed=42):
  import random
  import numpy as np
  random.seed(seed)
  np.random.seed(seed)
  torch.manual_seed(seed)
  torch.cuda.manual_seed(seed)
  torch.cuda.manual_seed_all(seed)
  torch.backends.cudnn.deterministic=True
  torch.backends.cudnn.benchmark = False

# Metric helper method
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

def compute_metrics(p):
    predictions, labels = p
    # Get the predicted labels by taking the argmax of logits
    preds = predictions.argmax(axis=-1)
    
    # Compute accuracy
    accuracy = accuracy_score(labels, preds)
    
    # Compute precision, recall, and F1 score for both macro and micro averages
    precision_macro = precision_score(labels, preds, average='macro')
    recall_macro = recall_score(labels, preds, average='macro')
    f1_macro = f1_score(labels, preds, average='macro')
    
    precision_micro = precision_score(labels, preds, average='micro')
    recall_micro = recall_score(labels, preds, average='micro')
    f1_micro = f1_score(labels, preds, average='micro')

    # Return the computed metrics
    metrics =  {
        'accuracy': accuracy,
        'precision_macro': precision_macro,
        'recall_macro': recall_macro,
        'f1_macro': f1_macro,
        'precision_micro': precision_micro,
        'recall_micro': recall_micro,
        'f1_micro': f1_micro
    }
    wandb.log(metrics)
    return metrics


# Add a custom callback to ensure loss logging
class WandbCallback(TrainerCallback):
    def on_log(self, args, state, control, logs=None, **kwargs):
        if not logs:
            return
        # Make sure we're logging the loss
        if "loss" in logs:
            wandb.log({"training_loss": logs["loss"]})
        # Log all other metrics
        wandb.log(logs)

train_files_path = '/home/abdoah/TND/legal-bert/train-files.txt'
eval_files_path = '/home/abdoah/TND/legal-bert/eval-files.txt'
data_path = '/home/abdoah/data/echr-processed'

tokenizer_name = 'allenai/longformer-base-4096'
model_name = 'allenai/longformer-base-4096'

max_length = 4096

tokenizer = LongformerTokenizer.from_pretrained(model_name)

train_dataset = ECHRDataset(train_files_path, data_path, tokenizer, max_length)
eval_dataset = ECHRDataset(eval_files_path, data_path, tokenizer, max_length)

print("Train dataset size:", len(train_dataset))
print("Eval dataset size:", len(eval_dataset))


data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
model = LongformerForSequenceClassification.from_pretrained(model_name, num_labels=3, gradient_checkpointing=True)
 

from transformers import Trainer, TrainingArguments

training_args = TrainingArguments(
    output_dir="./results_longformer_3_classes",
    learning_rate=1e-5,
    fp16=True,  # Enable mixed precision
    per_device_train_batch_size=2,  # Start with 2
    gradient_accumulation_steps=4,   # This gives effective batch size of 8
    per_device_eval_batch_size=2,
    num_train_epochs=5,
    weight_decay=0.01,
    logging_dir="./logs",
    do_eval = True,
    evaluation_strategy='steps',
    eval_steps=200,  # how often to evaluate
    save_strategy='steps',
    save_steps=1000,  # how often to save
    load_best_model_at_end=True,
    metric_for_best_model = 'f1_macro',
    greater_is_better = True,
    report_to='wandb',  # Disable wandb integration#
    log_level='info',
    logging_steps=200,  # Log every n steps
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
    callbacks=[WandbCallback()]
)

set_seed(training_args.seed)
trainer.train()

trainer.evaluate()

wandb.finish()