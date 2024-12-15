import os
import ollama
from groq import Groq
from openai import OpenAI
from dotenv import load_dotenv
from prompts import SENIOR_MIXTRAL_USER_PROMPT, SENIOR_LLAMA_USER_PROMPT

load_dotenv()

USER_PROMPT_OLD = f"""
            you are expert legal lawyer and expert at ECHR legal cases.
            carefully use the given facts of a legal case and conclusion, then are asked to identify the arguments provided for justifying the application of legal norms to the specific facts of the case.

            To do so, you have acess to an assisstant that can help you answer the questions you want to ask to be able to do the task.
            Collect the information you need to do the task, and then provide the reasoning behind the court decision.

            please ask one question at a time and wait for the answer before asking the next question.
            use the following format:
            Question: the question you want to ask
            Stop: to stop asking questions
            Final Answer: to provide the reasoning behind the court decision
         """
USER_PROMPT_1 = """
You are a legal expert specializing in European Court of Human Rights (ECHR) jurisprudence. Your task is to analyze the provided case facts and determine whether there has been a violation of the specified ECHR article. You should construct a structured legal analysis by gathering relevant information through targeted questions.

Guidelines:
- Ask one question at a time
- Wait for an answer before proceeding to the next question
- Focus on legal reasoning that would justify or refute a violation
- Consider both substantive and procedural aspects
- Examine relevant ECHR precedents and principles

Format:
Question: [Your specific question about the case facts or legal context]
Analysis: [Provide a structured legal analysis following this framework:]
1. Identification of the legal issue
2. Applicable legal principles and standards
3. Analysis of the facts against these standards
4. Reasoned conclusion about the violation
"""


class SeniorAgent:
    def __init__(self, backend="groq", model_name="llama3-8b-8192", cache=None):
        self.model_name = model_name
        self.cache = cache
        self.backend = backend
        self.model_name = model_name
        self.token_limit = 7500

        if backend == "groq":
            self.groq_client = Groq(api_key=os.getenv("GROQ_API_TOKEN"))
        elif backend == "openai":
            self.openai_client = OpenAI()

    def __str__(self) -> str:
        s = f"SummaryAgent(model_name={self.model_name})"
        for key, value in self.cache.items():
            s += f"\n{key}: {value}"
        return s

    def get_completion(self, prompt, system_message="You are a helpful assistant."):
        if self.backend == "ollama":
            response = ollama.chat(
                model=self.model_name,  # "llama3:8b",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
            )
            return response["message"]["content"]
        elif self.backend == "groq":
            chat_completion = self.groq_client.chat.completions.create(
                model=self.model_name,  # "llama3-70b-8192",
                temperature=0,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
            )
            return chat_completion.choices[0].message.content
        elif self.backend == "openai":
            completion = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
            )
            return completion.choices[0].message.content
        else:
            raise ValueError("Please provide a valid inference: 'ollama' or 'groq'")

    def init_classify(self, system_message="You are a helpful assistant."):
        # print("   init_classify ....")
        system_message = (
            "You are expert legal lawyer with European Court of Human Rights (ECHR)."
        )
        user_prompt = None
        if "mixtral" in self.model_name:
            user_prompt = SENIOR_MIXTRAL_USER_PROMPT
        elif "gemma" in self.model_name:
            user_prompt = SENIOR_MIXTRAL_USER_PROMPT
        elif "llama" in self.model_name:
            user_prompt = SENIOR_LLAMA_USER_PROMPT
        else:
            raise NotImplementedError(
                f"The prompt for the model {self.model_name} is not defined in prompts.py."
            )

        if self.cache is None:
            response = self.get_completion(user_prompt, system_message)
            self.cache = user_prompt + response
        else:
            user_prompt = self.cache
            response = self.get_completion(user_prompt, system_message)
            self.cache += "\n" + response
        return response

    def assign_cache(self, cache):
        self.cache = cache

    def append_to_cache(self, response):
        self.cache += "\n" + response

    def ask_question(self):
        imp_class = self.init_classify()

        return imp_class
