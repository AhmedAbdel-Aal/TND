from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from typing import Type
from utils import load_json


class FileInput(BaseModel):
    file_path: str = Field(description="Path to the case file to analyze")


class CaseFactsReader(BaseTool):
    name: str = "legal_case_reader"
    description: str = """Read the case and return the case text and metadata."""
    args_schema: Type[BaseModel] = FileInput

    def _run(self, file_path) -> str:
        # Always use the initialized file path
        try:
            file_path = file_path.strip()
            case_data = load_json(file_path)
            return case_data["facts"]  # ['THE FACTS']

        except Exception as e:
            return f"Error reading or analyzing file: {str(e)}"
