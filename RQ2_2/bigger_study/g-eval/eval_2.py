import os
import ollama
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class EvalTwoAgent:
    def __init__(self, backend="groq", model_name="llama3-8b-8192"):
        self.model_name = model_name
        self.cache = {}
        self.backend = backend
        self.model_name = model_name
        self.token_limit = 7500

        if backend == "groq":
            self.groq_client = Groq(api_key=os.getenv("GROQ_API_TOKEN"))

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
        else:
            raise ValueError("Please provide a valid inference: 'ollama' or 'groq'")

    def _generate(
        self,
        first_document,
        second_document,
        system_message="You are a helpful assistant.",
    ):
        system_message = (
            "You are expert legal lawyer with European Court of Human Rights (ECHR)."
        )

        user_prompt = f"""
            please read the two documents of a legal case and evaluate the second document based on the following critieria:.
            1. Determine if there is a Misrepresentation of Central Legal Issues.
            2. If there is a Failure to Recognize Nuances in Legal Concepts and Articles.
            3. If there is Incorrect Application of Legal Standards.
            4. Inadequate Connection Between Legal Notions and Factual Circumstances



            <first_document>
            {first_document}
            </first_document>

            <second_document>
            {second_document}
            </second_document>

            """
        # print(user_prompt)
        response = self.get_completion(user_prompt, system_message)
        self.cache["summary"] = response
        return response

    def generate(self, first_document, second_document):
        response = self._generate(first_document, second_document)

        return response
