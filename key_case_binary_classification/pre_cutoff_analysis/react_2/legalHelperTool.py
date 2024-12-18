from langchain.tools import BaseTool
import ast
from pydantic import BaseModel, Field, PrivateAttr
from langchain.chat_models import ChatOpenAI
from typing import Type
from utils import load_json


class LegalQuestion(BaseModel):
    file_path: str = Field(description="Path to the case file to analyze")
    question: str = Field(
        description="The specific question to address regarding the legal principles"
    )


class LegalHelper(BaseTool):
    name: str = "legal_helper_tool"
    description: str = """Answer EHCR legal Questions."""
    args_schema: Type[BaseModel] = LegalQuestion

    def __init__(self):
        super().__init__()

    def _get_prompt(self, case_facts, case_law, question) -> str:
        prompt = f"""You are a specialist in European Court of Human Rights (ECHR) jurisprudence.

            Your task is to answer legal question given the case facts and law:

            case facts:
            {case_facts}

            case law:
            {case_law}

            question:
            {question}

            Answer:
        """
        return prompt

    def _run(self, input) -> str:
        # Always use the initialized file path
        try:
            # print("input", input)
            parsed_input = ast.literal_eval(input) if isinstance(input, str) else input
            file_path, question = parsed_input[0], parsed_input[1]
            # print("question", question)
            # print("file_path", file_path)

            file_path = file_path.strip()
            case_data = load_json(file_path)
            case_facts = case_data["facts"]
            case_law = case_data["law"]

            llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
            prompt = self._get_prompt(case_facts, case_law, question)
            output = llm.predict(prompt)
            return output
        except Exception as e:
            return f"Error reading or analyzing file: {str(e)}"
