import os
import ollama
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

USER_PROMPT = f"""
            you are expert legal lawyer and expert at ECHR legal cases.
            you are asked to find out why the court assigned this case the given importane score,
            the reason should show the relation between facts, procedure, legal arguments, and the importance of the case.
            you have acess to an assisstant that can help you answer the questions you want to ask to be able to do the task.
            Collect as much information as you need to do the task, and then provide the reasoning behind the court decision.

            The labeling criteria is as follows:

                - High: All judgments, decisions, and advisory opinions that make a significant contribution to the development, clarification or modification of its case law, either generally or in relation to a particular State.
                - Medium: Other judgments, decisions and advisory opinions which, while not making a significant contribution to the case-law, nevertheless go beyond merely applying existing case-law.
                - Low: Judgments, decisions and advisory opinions of little legal interest, namely judgments and decisions that simply apply existing case-law, friendly settlements and strike outs (unless raising a particular point of interest).

            please ask one question at a time and wait for the answer before asking the next question.
            use the following format:
            Question: the question you want to ask
            Stop: to stop asking questions
            Final Answer: to provide the reasoning behind the court decision
         """


class SeniorAgent:
    def __init__(self, backend="groq", model_name="llama3-8b-8192"):
        self.model_name = model_name
        self.cache = None
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
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
            )
            return chat_completion.choices[0].message.content
        else:
            raise ValueError("Please provide a valid inference: 'ollama' or 'groq'")

    def init_classify(self, system_message="You are a helpful assistant."):
        # print("   init_classify ....")
        system_message = (
            "You are expert legal lawyer with European Court of Human Rights (ECHR)."
        )

        if self.cache is None:
            user_prompt = USER_PROMPT
            response = self.get_completion(user_prompt, system_message)
            self.cache = user_prompt + response
        else:
            user_prompt = self.cache
            response = self.get_completion(user_prompt, system_message)
            self.cache += response
        return response

    def append_to_cache(self, response):
        self.cache += response

    def ask_question(self):
        imp_class = self.init_classify()

        return imp_class
