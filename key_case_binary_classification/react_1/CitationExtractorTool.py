from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from typing import Type
from utils import load_json


class FileInput(BaseModel):
    file_path: str = Field(description="Path to the case file to analyze")


class CitationExtractor(BaseTool):
    name: str = "legal_principle_extractor"
    description: str = """Extract key legal principles from the case file."""
    args_schema: Type[BaseModel] = FileInput

    def _get_prompt(self, case_facts, law) -> str:
        prompt = f"""You are a specialist in European Court of Human Rights (ECHR) jurisprudence.

            Analyze these case facts and provide:


            1. CHRONOLOGICAL CASE LIST:
            For each cited case, provide:
            - Full case name
            - Date
            - Analyze WHY this case was cited. For example:
                - Similar factual circumstances
                - Previous legal reasoning being applied
                - Established principles being referenced
                - Procedural precedents
                - Other reasons
            - Analyze HOW this case was cited. For example:
                - Direct application of precedent
                - Extension of previous principles
                - Distinguishing from previous case
                - Clarifying previous interpretation
                - Other approaches

            Case Facts:
            {case_facts}

            Case Law Section:
            {law}

            Cited ECHR Cases:
        """
        return prompt

    def _run(self, file_path: str = None) -> str:
        # Always use the initialized file path
        try:
            file_path = file_path.strip()
            case_data = load_json(file_path)
            case_facts = case_data["facts"]  # ['THE FACTS']
            law = case_data["law"]  # ['THE LAW']

            llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
            prompt = self._get_prompt(case_facts, law)
            return llm.predict(prompt)
        except Exception as e:
            return f"Error reading or analyzing file: {str(e)}"
