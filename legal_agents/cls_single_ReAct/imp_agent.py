import os
import ollama
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class ImpAgent:
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
            Please classify a case into one of three categories of importance: [High, Medium, Low],
            you should provide reasons for your classification,
            the reason should show the relation between facts, procedure, legal arguments, and the importance of the case,
            Label the cases with an importance score based on the following criteria,:

            High: All judgments, decisions, and advisory opinions that make a significant contribution
            to the development, clarification or modification of its case law,
            either generally or in relation to a particular State.

            Medium: Other judgments, decisions and advisory opinions which, while
            not making a significant contribution to the case-law, nevertheless go beyond merely
            applying existing case-law.

            Low: Judgments, decisions and advisory opinions of little legal interest,
            namely judgments and decisions that simply apply existing case-law, friendly
            settlements and strike outs (unless raising a particular point of interest).


            The source text and initial summary, delimited by XML tags <SOURCE_TEXT></SOURCE_TEXT> as follows:

            <SOURCE_TEXT>
            {source_text}
            </SOURCE_TEXT>

            Let's think step by step about the importance of the case and classify it into one of the three categories with reasoning:
         """
        response = self.get_completion(user_prompt, system_message)
        self.cache["summary"] = response
        return response

    def classify(self, source_text):
        imp_class = self.init_classify(source_text)

        return imp_class
