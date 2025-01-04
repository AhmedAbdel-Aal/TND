import torch
import numpy as np
import pandas as pd
from transformers import LongformerTokenizer, LongformerForSequenceClassification, Trainer, TrainingArguments
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from data import ECHRDataset  # Make sure this is in the same directory

def compute_metrics(p):
    predictions, labels = p
    preds = predictions.argmax(axis=-1)
    
    accuracy = accuracy_score(labels, preds)
    precision_macro = precision_score(labels, preds, average='macro')
    recall_macro = recall_score(labels, preds, average='macro')
    f1_macro = f1_score(labels, preds, average='macro')
    
    precision_micro = precision_score(labels, preds, average='micro')
    recall_micro = recall_score(labels, preds, average='micro')
    f1_micro = f1_score(labels, preds, average='micro')

    return {
        'accuracy': accuracy,
        'precision_macro': precision_macro,
        'recall_macro': recall_macro,
        'f1_macro': f1_macro,
        'precision_micro': precision_micro,
        'recall_micro': recall_micro,
        'f1_micro': f1_micro
    }

def main():
    # Paths
    model_path = "/home/abdoah/TND/legal-bert/results_longformer_3_classes/checkpoint-9745"  # Path to your saved model
    eval_files_path = '/home/abdoah/TND/legal-bert/eval-files.txt'
    data_path = '/home/abdoah/data/echr-processed'
    tokenizer_name = 'allenai/longformer-base-4096'
    max_length = 4096

    # Load tokenizer and create dataset
    tokenizer = LongformerTokenizer.from_pretrained(tokenizer_name)
    eval_dataset = ECHRDataset(eval_files_path, data_path, tokenizer, max_length)
    
    # Load model
    model = LongformerForSequenceClassification.from_pretrained(model_path)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    # Training arguments (only needed for the Trainer)
    training_args = TrainingArguments(
        output_dir="./eval_results",
        per_device_eval_batch_size=2,
        fp16=True
    )

    # Create trainer for evaluation
    trainer = Trainer(
        model=model,
        args=training_args,
        eval_dataset=eval_dataset,
        compute_metrics=compute_metrics
    )

    # Get predictions
    print("\nGenerating predictions...")
    predictions = trainer.predict(eval_dataset)
    # Print results
    print("\nEvaluation Results:")
    for key, value in predictions.metrics.items():
        print(f"{key}: {value}")


    pred_labels = np.argmax(predictions.predictions, axis=-1)
    probabilities = predictions.predictions
    # Get item IDs from the dataset
    item_ids = [eval_dataset[i]["itemid"] for i in range(len(eval_dataset))]

    # Or save to CSV
    results_df = pd.DataFrame({
        'itemid': item_ids,
        'predicted_label': pred_labels,
        'true_label': predictions.label_ids,
        'probability_class_0': probabilities[:, 0],
        'probability_class_1': probabilities[:, 1],
        'probability_class_2': probabilities[:, 2]
    })
    
    # Save to CSV
    results_df.to_csv('predictions_with_ids.csv', index=False)
    print("\nPredictions saved to 'predictions.csv'")

if __name__ == "__main__":
    main()