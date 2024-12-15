from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from typing import Type
from utils import load_json


class FileInput(BaseModel):
    file_path: str = Field(description="Path to the case file to analyze")


class LegalPrincipleExtractor(BaseTool):
    name: str = "legal_principle_extractor"
    description: str = """Extract key legal principles from the case file."""
    args_schema: Type[BaseModel] = FileInput

    def _get_prompt(self, case_facts) -> str:
        prompt = f"""You are a specialist in European Court of Human Rights (ECHR) jurisprudence. The ECHR is established under the European Convention on Human Rights, protecting fundamental rights across Council of Europe member states.

            Analyze these case facts and provide:

            KEY LEGAL PRINCIPLES:
            - Extract the main legal principles discussed or applied
            - Show how each principle relates to specific ECHR Articles
            - Note any conflicts or balancing between principles

            Please provide a structured analysis that clearly maps principles to Articles.

            Case Facts:

            {case_facts}
        """
        return prompt

    def _run(self, file_path: str = None) -> str:
        # Always use the initialized file path
        try:
            file_path = file_path.strip()
            case_data = load_json(file_path)
            case_facts = case_data["facts"]

            llm = ChatOpenAI(temperature=0, model_name="gpt-4o")
            prompt = self._get_prompt(case_facts)
            return llm.predict(prompt)
        except Exception as e:
            return f"Error reading or analyzing file: {str(e)}"
