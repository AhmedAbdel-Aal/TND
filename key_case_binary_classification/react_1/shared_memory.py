# shared_memory.py
import json
from utils import load_json


class SharedMemory:
    def __init__(self, file_path: str = None):
        self.file_path = file_path
        self.data = {}

    def load_case(self, file_path: str):
        try:
            self.data = load_json(file_path)
        except Exception as e:
            print(f"Error loading case file {file_path}: {str(e)}")

    def get_facts(self):
        return self.data.get("facts", "")

    def get_law(self):
        return self.data.get("law", "")
