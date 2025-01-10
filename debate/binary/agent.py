"class Agent"
import os
import dotenv
from utils import text_to_json
from llm import llm_call

dotenv.load_dotenv()


class Agent:
    def __init__(self, name: str, backend: str, system_prompt: str = NotImplemented):
        self.name = name
        self.backend = backend
        self.system_prompt = system_prompt
        self.context = []
        self.latest_response = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def call(self):
        reponse = llm_call(self.context, self.backend)
        return reponse

    def add_to_context(self, role, content):
        s = {"role": role, "content": content}
        self.context.append(s)

    def get_latest_response(self):
        for item in reversed(self.context):
            if item["role"] == "assistant":
                return item["content"]

    def get_context(self):
        return self.context

    def get_trace(self):
        trace = {}
        round = 1
        for item in self.context:
            if item["role"] == "assistant":
                parsed_response = text_to_json(item["content"])
                # parsed_response['round'] = round
                trace["round_" + str(round)] = parsed_response
                # trace.append(parsed_response)
                round += 1
            else:
                continue
        return trace
