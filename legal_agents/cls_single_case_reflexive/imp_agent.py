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

    def init_classify(
        self, source_text, principles, system_message="You are a helpful assistant."
    ):
        print("   init_classify ....")
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


            The source text and initial summary, delimited by XML tags <SOURCE_TEXT></SOURCE_TEXT> and <LEGAL_PRINCIPLES></LEGAL_PRINCIPLES>, are as follows:

            <SOURCE_TEXT>
            {source_text}
            </SOURCE_TEXT>

            <LEGAL_PRINCIPLES>
            {principles}
            </LEGAL_PRINCIPLES>

            importance class:
         """
        response = self.get_completion(user_prompt, system_message)
        self.cache["summary"] = response
        return response

    def reflect(self, source_text, principles, imp_class):
        print("   reflect ....")
        system_message = (
            "You are expert legal lawyer with European Court of Human Rights (ECHR)."
        )
        reflection_print = f"""
            Your task is to carefully read a legal summary text with highlighted legal principles and the given importance class,
            and then give constructive criticism and helpful suggestions. \

            The source text and initial summary, delimited by XML tags <SOURCE_TEXT></SOURCE_TEXT> and <LEGAL_PRINCIPLES></LEGAL_PRINCIPLES>, are as follows:

            <SOURCE_TEXT>
            {source_text}
            </SOURCE_TEXT>

            <LEGAL_PRINCIPLES>
            {principles}
            </LEGAL_PRINCIPLES>

            <IMPORTANCE_CLASS>
            {imp_class}
            </IMPORTANCE_CLASS>

            When writing suggestions, pay attention to whether there are ways to improve the  given importance class' \n\

                (i) impact (by ensuring it reflects the legal impact of the case details on the law),
                (ii) application (by ensuring if it just applying existing law or imposing new interpretations),
                (iii) contribution (by ensuring if it makes a significant contribution to the case-law, nevertheless go beyond merely
            applying existing case-law)

            Write a list of specific, helpful and constructive suggestions for improving the given importance class.
            Output only the suggestions and nothing else.

            Here is a list of suggestions:
        """
        response = self.get_completion(reflection_print, system_message)
        self.cache["reflection"] = response
        return response

    def improve(self, source_text, principles, imp_class, reflection):
        print("   improve ....")
        system_message = (
            "You are expert legal lawyer with European Court of Human Rights (ECHR)."
        )
        reflection_print = f"""
                Your task is to carefully read, then reclassify the importance score of legal case into
                one of three classes [high, Medium, Low], taking into account a list of expert suggestions and constructive criticisms.

                The source text, the extarcted legal principles, th given importance class, and the legal expert suggestions are delimited by XML tags <SOURCE_TEXT></SOURCE_TEXT>, <SUMMARY></SUMMARY> and <EXPERT_SUGGESTIONS></EXPERT_SUGGESTIONS> \
                as follows:

                <SOURCE_TEXT>
                {source_text}
                </SOURCE_TEXT>

                <LEGAL_PRINCIPLES>
                {principles}
                </LEGAL_PRINCIPLES>

                <IMPORTANCE_CLASS>
                {imp_class}
                </IMPORTANCE_CLASS>

                <EXPERT_SUGGESTIONS>
                {reflection}
                </EXPERT_SUGGESTIONS>

                Please take into account the expert suggestions when deciding on the new importance class. reclassify the importance by ensuring:

                (i) impact (by ensuring it reflects the legal impact of the case details on the law),
                (ii) application (by ensuring if it just applying existing law or imposing new interpretations),
                (iii) contribution (by ensuring if it makes a significant contribution to the case-law, nevertheless go beyond merely
            applying existing case-law)

                Here is the new importance class:
            """
        response = self.get_completion(reflection_print, system_message)
        self.cache["improvment"] = response
        return response

    def classify(self, source_text, principles):
        imp_class = self.init_classify(source_text, principles)
        reflection = self.reflect(source_text, principles, imp_class)
        improved_summary = self.improve(source_text, principles, imp_class, reflection)

        return improved_summary
