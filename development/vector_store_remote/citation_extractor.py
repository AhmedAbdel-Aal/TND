from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from typing import Type
from utils import load_json
import os


class FileInput(BaseModel):
    file_path: str = Field(description="Path to the case file to analyze")


class CitationExtractor(BaseTool):
    name: str = "citation_extractor"
    description: str = """Extract citations from the case file."""
    args_schema: Type[BaseModel] = FileInput

    def _get_prompt(self, case_facts, law) -> str:
        prompt = f"""You are a specialist in European Court of Human Rights (ECHR) jurisprudence.
        Analyze these case facts and return a JSON array with the following structure for each cited case:
        [
            {{
                "case_name": "Full case name",
                "date": "Date of the case",
            }}
        ]

        Case Facts:
        {case_facts}

        Case Law:
        {law}
        """
        return prompt


    def _run(self, file_path: str = None) -> str:
        # Always use the initialized file path
        file_path = file_path.strip()
        try:
            case_data = load_json(file_path)
            case_facts = case_data["facts"]  # ['THE FACTS']
            law = case_data["law"]  # ['THE LAW']

            llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
            prompt = self._get_prompt(case_facts, law)
            return llm.predict(prompt)
        except Exception as e:
            return f"Error reading or analyzing file: {str(e)}"
