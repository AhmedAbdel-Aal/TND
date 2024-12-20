from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_anthropic import ChatAnthropic
from typing import Dict
from prompts import get_prompt


class LegalCaseClassifier:
    def __init__(
        self,
        prompt_id,
        backend="openai",
        model_name: str = "gpt-4o-mini",
        temperature: float = 0,
    ):
        self.openai = ChatOpenAI(model_name=model_name, temperature=temperature)
        # self.groq = ChatGroq(model="mixtral-8x7b-32768", temperature=0)
        # self.anthropic = ChatAnthropic(model='claude-3-haiku-20240307')

        self.llm = None
        if backend == "openai":
            self.llm = self.openai
        elif backend == "groq":
            self.llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)
        elif backend == "anthropic":
            self.llm = ChatAnthropic(model="claude-3-haiku-20240307")
        else:
            self.llm = self.openai

        # Step 1: Detailed Legal Analysis Prompt
        self.classification_prompt = get_prompt(prompt_id)

        # Create the chains
        self.classification_chain = LLMChain(
            llm=self.llm, prompt=self.classification_prompt
        )

    def classify_case(self, **kwargs) -> Dict[str, any]:
        # Make classification based on case facts
        classification_result = self.classification_chain.run(**kwargs)

        # Extract final classification
        if (
            "CLASSIFICATION: KEY CASE" in classification_result
            or "Key Case" in classification_result
        ):
            classification = "KEY CASE"
        elif (
            "CLASSIFICATION: NOT KEY CASE" in classification_result
            or "Non-Key Case" in classification_result
        ):
            classification = "NOT KEY CASE"
        else:
            classification = "-1"

        return {
            "classification": classification,
            "classification_reasoning": classification_result,
        }
