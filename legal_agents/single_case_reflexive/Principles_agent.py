import os
import ollama
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class LPAgent:
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

    def init_extract(self, prompt, system_message="You are a helpful assistant."):

        print("   init_extract ....")
        system_message = (
            "You are expert legal lawyer with European Court of Human Rights (ECHR)."
        )

        user_prompt = f"""
            Please list the legal principles in the following legal case.
            case: {prompt}
            legal principles:       
         """
        response = self.get_completion(user_prompt, system_message)
        self.cache["summary"] = response
        return response

    def reflect(self, source_text, principles):

        print("   reflect ....")
        system_message = (
            "You are expert legal lawyer with European Court of Human Rights (ECHR)."
        )
        reflection_print = f"""
            Your task is to carefully read a legal summary text and the extracted legal principles,
            and then give constructive criticism and helpful suggestions. \

            The source text and initial summary, delimited by XML tags <SOURCE_TEXT></SOURCE_TEXT> and <LEGAL_PRINCIPLES></LEGAL_PRINCIPLES>, are as follows:

            <SOURCE_TEXT>
            {source_text}
            </SOURCE_TEXT>

            <LEGAL_PRINCIPLES>
            {principles}
            </LEGAL_PRINCIPLES>

            When writing suggestions, pay attention to whether there are ways to improve the extracted legal principles's \n\
            
                (i) accuracy (by ensuring it correctly reflects all legal principles of the source text),
                (ii) conciseness (by removing unnecessary details and repetitions), \
                (iii) clarity (by ensuring the summary is easy to understand),
                (iv) coverage (by including all legal principles mentioned in the source text).
            
            Write a list of specific, helpful and constructive suggestions for improving the extracted legal principles.
            Output only the suggestions and nothing else.
            
            Here is a list of suggestions:
        """
        response = self.get_completion(reflection_print, system_message)
        self.cache["reflection"] = response
        return response

    def improve(self, source_text, principles, reflection):

        print("   improve ....")
        system_message = (
            "You are expert legal lawyer with European Court of Human Rights (ECHR)."
        )
        reflection_print = f"""
                Your task is to carefully read, then edit a list of legal principles, taking into
                account a list of expert suggestions and constructive criticisms.

                The source text, the initial summary, and the legal expert suggestions are delimited by XML tags <SOURCE_TEXT></SOURCE_TEXT>, <SUMMARY></SUMMARY> and <EXPERT_SUGGESTIONS></EXPERT_SUGGESTIONS> \
                as follows:

                <SOURCE_TEXT>
                {source_text}
                </SOURCE_TEXT>

                <LEGAL_PRINCIPLES>
                {principles}
                </LEGAL_PRINCIPLES>

                <EXPERT_SUGGESTIONS>
                {reflection}
                </EXPERT_SUGGESTIONS>

                Please take into account the expert suggestions when editing the summary. Edit the summary by ensuring:

                (i) accuracy (by ensuring it correctly reflects all legal principles of the source text),
                (ii) conciseness (by removing unnecessary details and repetitions), \
                (iii) clarity (by ensuring the summary is easy to understand),
                (iv) coverage (by including all legal principles mentioned in the source text).

                Output only the new list of legal principles and nothing else.
                
                Here is the revised list of legal principles:
            """
        response = self.get_completion(reflection_print, system_message)
        self.cache["improvment"] = response
        return response

    def extract_lps(self, source_text):

        principles = self.init_extract(source_text)
        reflection = self.reflect(source_text, principles)
        improved_summary = self.improve(source_text, principles, reflection)

        return improved_summary
