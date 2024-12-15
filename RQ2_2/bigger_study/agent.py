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
        self, facts, conclusion, system_message="You are a helpful assistant."
    ):
        # print("   init_classify ....")
        system_message = (
            "You are expert legal lawyer with European Court of Human Rights (ECHR)."
        )

        user_prompt = f"""
            Your task is to carefully read the facts of a legal case and conclusion,
            then identify the arguments provided for justifying the application of legal norms to the specific facts of the case.

            1. Identify general legal norms and principles.

            2. Make sure description of circumstances and requirements provided as criteria for a legal doctrines match.

            3. Map key words like ‘sometimes’, ‘exceptionally’, ‘in the present case’ with the view to make sure that there is correspondence between legal standards and circumstances;

            4. Focus on key phrases detailing the application of substantive or procedural limb/branch explaining the scope of application of the Article;

            5. Make sure to map accordingly key phrases which detail the application of the Article to a variety to persons such as victims, state agents, witnesses, relatives and similar;

            6. Make sure to map accordingly key phrases which detail the application of the Article depending on jurisdiction, material or temporal and those which detail the repartition or just satisfaction;

            7. Distinguish conditions for the application of Articles across various contexts.

            8. Carefully identify key phrases which describe choices from key phrases which describe responsibility and accountability

            9. Highlight hey phrases which describe thresholds/conditions.

            The facts section is given between XML tags <FACTS></FACTS> <CONCLUSION></CONCLUSION>  as follows:

            <FACTS>
            {facts}
            </FACTS>

            <CONCLUSION>
            {conclusion}
            </CONCLUSION>

            reasoning:
         """
        response = self.get_completion(user_prompt, system_message)
        self.cache["summary"] = response
        return response

    def generate(self, facts, conclusion):
        imp_class = self.init_classify(facts, conclusion)

        return imp_class
