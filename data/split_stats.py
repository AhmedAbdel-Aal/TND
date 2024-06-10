import os
import json
from collections import defaultdict
from tqdm import tqdm

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def count_labels_in_directory(directory):
    label_counts = defaultdict(int)
    for filename in tqdm(os.listdir(directory)):
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            data = load_json(file_path)
            label = data.get('importance', None)
            if label is not None:
                label_counts[label] += 1
            if int(label) == 1:
                print(f"Found label 1 in file {data.get('itemid', None)}")
    return label_counts

if __name__ == "__main__":
    train_directory = './train'
    dev_directory = './dev'
    test_directory = './test'
    
    print("Counting labels in train directory...")
    train_label_counts = count_labels_in_directory(train_directory)

    print("Counting labels in dev directory...")
    dev_label_counts = count_labels_in_directory(dev_directory)

    print("Counting labels in test directory...")
    test_label_counts = count_labels_in_directory(test_directory)
    
    print("Label distribution in train directory:")
    for label, count in train_label_counts.items():
        print(f"Label {label}: {count} files")
   
    print("Label distribution in dev directory:")
    for label, count in dev_label_counts.items():
        print(f"Label {label}: {count} files")
    
    print("Label distribution in test directory:")
    for label, count in test_label_counts.items():
        print(f"Label {label}: {count} files")
