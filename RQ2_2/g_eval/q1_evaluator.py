import os
import ollama
import anthropic
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class Q1Evaluator:
    def __init__(self, backend="groq", model_name="llama3-8b-8192"):
        self.model_name = model_name
        self.cache = {}
        self.backend = backend
        self.token_limit = 7500

        if backend == "groq":
            self.groq_client = Groq(api_key=os.getenv("GROQ_API_TOKEN"))
        if backend == "anthropic":
            self.anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC"))

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
            print("   get_completion from groq....")
            chat_completion = self.groq_client.chat.completions.create(
                model="llama3-70b-8192",
                temperature=0,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
            )
            return chat_completion.choices[0].message.content
        elif self.backend == "anthropic":
            chat_completion = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1024,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
            )
            return chat_completion.content
        else:
            raise ValueError("Please provide a valid inference: 'ollama' or 'groq'")

    def init_classify(
        self, law, generated_reasoning, system_message="You are a helpful assistant."
    ):
        # print("   init_classify ....")
        system_message = (
            "You are expert legal lawyer with European Court of Human Rights (ECHR)."
        )

        user_prompt = f"""
            You are an expert in European Court of Human Rights (ECHR) case law.
            You are given the law section of a case, and the generated reasoning by a lawyer.
            Your task is to rate the generated reasoning compared against the actual law section of the case.

            Evaluation Criteria:

            - Identification of main elements of the precedents/legal notion (identification of articles)

            Evaluation Steps:

            1. Read the actual law section and identify the main elements of the precedents/legal notion
            2. Read the generated law section and compare it to the actual law section. Check if the generated reasoning covers the main elements of the precedents/legal notion.
            3. Assign a score for Q1 on a scale of 1 to 5, where 1 = Poor 2 = Fair 3 = Good 4 = Very Good 5 = Excellent.
            4. Explain the reasoning behind your score in the Evaluation Form.

            Example:

            <LAW>
            {law}
            </LAW>

            <GENERATED_REASONING>
            {generated_reasoning}
            </GENERATED_REASONING>

            use the following format:
            score:
            explanation:
         """
        response = self.get_completion(user_prompt, system_message)
        self.cache["summary"] = response
        return response

    def evaluate(self, law, generated_reasoning):
        imp_class = self.init_classify(law, generated_reasoning)

        return imp_class
