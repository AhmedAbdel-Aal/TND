import os
import ollama
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class QAgent:
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
            Answer the following question about summaized legal case, let's think step by step about the following questions:

            - Analyze the legal issue:

             - What is the primary legal question or issue addressed in this case?
             - Is this a novel issue or one that has been previously addressed by the court?

            - Examine the facts:

             - Are there any unique or unusual circumstances in this case?
             - Does the case involve a particularly vulnerable group or individual?
             - Is there a significant public interest element?

            - Consider the law applied:

             - Does the case involve the interpretation of a fundamental right or freedom?
             - Is there a conflict between different rights or principles?
             - Does the case clarify or expand on existing legal principles?


            - Evaluate the procedure:

             - At what level of the court system was the case decided?
             - Was it a Grand Chamber decision, indicating high importance?
             - Were there any interventions by third parties or other states?


            - Assess the conclusion:

             - Does the judgment establish a new legal principle or significantly modify existing case law?
             - Is the decision likely to have wide-ranging implications beyond this specific case?
             - Does it resolve a conflict in jurisprudence between different member states?


            - Consider the date:

             - Is this a recent case that addresses contemporary issues?
             - Does it revisit or update older principles in light of societal changes?


            - Reflect on potential impact:

             - Will this decision likely affect a large number of people or states?
             - Does it address a systemic issue within a member state or across multiple states?
             - Could it lead to changes in domestic legislation or practices?

            The summary is given by XML tags <SUMMARY></SUMMARY> as follows:

            <SUMMARY>
            {source_text}
            </SUMMARY>

            Answers to the questions:
         """
        response = self.get_completion(user_prompt, system_message)
        self.cache["summary"] = response
        return response

    def classify(self, source_text):
        imp_class = self.init_classify(source_text)

        return imp_class
