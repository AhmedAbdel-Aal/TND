import openai
import os
from typing import List, Dict
from langchain.chat_models import ChatOpenAI


def get_completion(prompt, model_name="gpt-4o-mini"):
    llm = ChatOpenAI(temperature=0, model_name=model_name)
    return llm.predict(prompt)
