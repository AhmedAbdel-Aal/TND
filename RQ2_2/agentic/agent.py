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

    def init_classify(
        self,
        facts_1,
        law_1,
        conclusion_1,
        facts_2,
        conclusion_2,
        system_message="You are a helpful assistant.",
    ):
        # print("   init_classify ....")
        system_message = (
            "You are expert legal lawyer with European Court of Human Rights (ECHR)."
        )

        user_prompt = f"""
            You are an expert in European Court of Human Rights (ECHR) case law. Given the following facts of a case and its conclusion, generate the "Law" section of an ECHR judgment. Your response should:
            You are given one example of facts and legal arguments below to help you understand the task.


            <FACTS>
            {facts_1}
            </FACTS>

            <CONCLUSION_1>
            {conclusion_1}
            </CONCLUSION_1>

            <LEGAL_ARGUMENTS>
            {law_1}
            </LEGAL_ARGUMENTS>

            <FACTS>
            {facts_2}
            </FACTS>

            <CONCLUSION_2>
            {conclusion_2}
            </CONCLUSION_2>

             <LEGAL_ARGUMENTS>:
         """
        response = self.get_completion(user_prompt, system_message)
        self.cache["summary"] = response
        return response

    def generate(self, facts_1, law_1, conclusion_1, facts_2, conclusion_2):
        imp_class = self.init_classify(
            facts_1, law_1, conclusion_1, facts_2, conclusion_2
        )

        return imp_class
