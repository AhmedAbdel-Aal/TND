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
        self, facts_1, law_1, facts_2, system_message="You are a helpful assistant."
    ):
        # print("   init_classify ....")
        system_message = (
            "You are expert legal lawyer with European Court of Human Rights (ECHR)."
        )

        user_prompt = f"""
            You are an expert in European Court of Human Rights (ECHR) case law. Given the following facts of a case, generate the "Law" section of an ECHR judgment. Your response should:

            1. Begin with a brief mention of the relevant Articles of the European Convention on Human Rights.

            2. Include subsections for:
            a) Relevant domestic law and practice
            b) Relevant international law (if applicable)
            c) Parties' submissions (arguments from both the applicant and the respondent state)
            d) The Court's assessment

            3. In the Court's assessment:
            - Apply established ECHR case law principles
            - Analyze the facts in light of the relevant Convention articles
            - Provide clear legal reasoning leading to a conclusion on whether there has been a violation

            4. Use formal, precise legal language typical of ECHR judgments.

            5. Maintain objectivity and impartiality in presenting arguments and reaching conclusions.

            6. Ensure logical flow and coherence in the legal argumentation.

            7. Reference relevant previous ECHR cases to support the legal reasoning.

            8. Conclude with a clear statement on whether there has been a violation of the Convention.

            You are given one example of facts and legal arguments below to help you understand the task.


            <FACTS>
            {facts_1}
            </FACTS>

            <LEGAL_ARGUMENTS>
            {law_1}
            </LEGAL_ARGUMENTS>

            <FACTS>
            {facts_2}
            </FACTS>

             <LEGAL_ARGUMENTS>:
         """
        response = self.get_completion(user_prompt, system_message)
        self.cache["summary"] = response
        return response

    def generate(self, facts_1, law_1, facts_2):
        imp_class = self.init_classify(facts_1, law_1, facts_2)

        return imp_class
