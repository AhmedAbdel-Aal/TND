import os
import shutil
from datetime import datetime
from tqdm import tqdm
import json

# Directory containing JSON files
directory_path = "./echr-processed"
train_directory = "./train"
dev_directory = "./dev"
test_directory = "./test"


def load_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def move_files_by_date(directory_path, train_directory, test_directory):
    # Ensure the train and test directories exist
    os.makedirs(train_directory, exist_ok=True)
    os.makedirs(dev_directory, exist_ok=True)
    os.makedirs(test_directory, exist_ok=True)

    # Process each file in the directory
    for filename in tqdm(os.listdir(directory_path)):
        if filename.endswith(".json"):
            file_path = os.path.join(directory_path, filename)
            data = load_json(file_path)

            date_string = data["judgementdate"]
            parsed_date = datetime.strptime(date_string, "%d/%m/%Y").date()

            # Determine the destination directory based on the date
            if parsed_date.year < 2013:
                dest_directory = train_directory
            elif parsed_date.year < 2015:
                dest_directory = dev_directory
            else:
                dest_directory = test_directory

            # Move the file to the appropriate directory
            shutil.move(file_path, os.path.join(dest_directory, filename))


if __name__ == "__main__":
    move_files_by_date(directory_path, train_directory, test_directory)
