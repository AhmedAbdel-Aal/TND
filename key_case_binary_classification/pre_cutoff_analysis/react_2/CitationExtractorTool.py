from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from typing import Type
from utils import load_json
from utils import load_json, from_input_path_to_output_path
import os


class FileInput(BaseModel):
    file_path: str = Field(description="Path to the case file to analyze")


class CitationExtractor(BaseTool):
    name: str = "citation_extractor"
    description: str = """Extract citations from the case file."""
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

    def check_cache(self, file_path):
        # get output file path
        output_file_path = from_input_path_to_output_path(file_path)
        # check if a result file exists
        exists = os.path.exists(output_file_path)

        # load log file
        if exists:
            log = load_json(output_file_path)
            tool_outputs = log["logs"]["tool_outputs"]
            for tool_output in tool_outputs:
                if tool_output["tool"] == "citation_extractor":
                    print(f"Tool Output Cache found: {tool_output['output'][:100]}")
                    return tool_output["output"]
        return None

    def _run(self, file_path: str = None) -> str:
        # Always use the initialized file path
        file_path = file_path.strip()
        cached_output = self.check_cache(file_path)
        if cached_output:
            return cached_output
        try:
            case_data = load_json(file_path)
            case_facts = case_data["facts"]  # ['THE FACTS']
            law = case_data["law"]  # ['THE LAW']

            llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
            prompt = self._get_prompt(case_facts, law)
            return llm.predict(prompt)
        except Exception as e:
            return f"Error reading or analyzing file: {str(e)}"
