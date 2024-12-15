import os
import ollama
from groq import Groq
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class JuniorAgent:
    def __init__(self, backend="groq", model_name="llama3-8b-8192"):
        self.model_name = model_name
        self.cache = {}
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

    def init_classify(
        self, facts, conclusion, question, system_message="You are a helpful assistant."
    ):
        # print("   init_classify ....")
        system_message = (
            "You are expert legal lawyer with European Court of Human Rights (ECHR)."
        )

        user_prompt = f"""
            you are expert legal lawyer and expert at ECHR legal cases.
            You are helping a senior lawyer with coming up with the reasoning behind the court decision.
            You task is to answer the following question about the given legal case facts and conclusion.
            you can't reply with question.
            you can't ask for more information.

            your answer should start with "Answer:"

            The facts, conclusion, and the question are given by XML tags <FACTS></FACTS>, <CONCLUSION></CONCLUSION>, <QUESTION></QUESTION> as follows:

            <FACTS>
            {facts}
            </FACTS>

            <CONCLUSION>
            {conclusion}
            </CONCLUSION>

            <QUESTION>
            {question}
            </QUESTION>

            Let's think step by step about the answer to the question.
            "Answer:"
         """
        # print(user_prompt)
        response = self.get_completion(user_prompt, system_message)
        self.cache["summary"] = response
        return response

    def answer_question(self, facts, conclusion, question):
        imp_class = self.init_classify(facts, conclusion, question)

        return imp_class
