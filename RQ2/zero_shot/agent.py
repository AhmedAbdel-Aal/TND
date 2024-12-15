import os
import ollama
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class Agent:
    def __init__(self, backend="groq", model_name="llama3-8b-8192"):
        self.model_name = model_name
        self.cache = {}
        self.backend = backend
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
                model="llama3:8b",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
            )
            return response["message"]["content"]
        elif self.backend == "groq":
            chat_completion = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
            )
            return chat_completion.choices[0].message.content
        else:
            raise ValueError("Please provide a valid inference: 'ollama' or 'groq'")

    def init_classify(self, source_text, system_message="You are a helpful assistant."):
        # print("   init_classify ....")
        system_message = (
            "You are expert legal lawyer with European Court of Human Rights (ECHR)."
        )

        user_prompt = f"""
            Your task is to carefully read the facts of a legal case, then give the legal arguments for this fact.
            Make sure to come up with coherent and legally sound arguments given the facts of a case.

            The facts section is given between XML tags <FACTS></FACTS> as follows:

            <FACTS>
            {source_text}
            </FACTS>

            :
         """
        response = self.get_completion(user_prompt, system_message)
        self.cache["summary"] = response
        return response

    def generate(self, source_text):
        imp_class = self.init_classify(source_text)

        return imp_class
