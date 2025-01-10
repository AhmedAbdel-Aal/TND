from openai import OpenAI
from typing import Dict
import dotenv
import os

dotenv.load_dotenv()

openai_client = OpenAI()
deepseek_client = OpenAI(
    api_key=os.environ["DEEP_SEEK"], base_url="https://api.deepseek.com"
)


def llm_call_deepseek(prompt):
    # print("backend used deepseek")
    response = deepseek_client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.",
            },
            {"role": "user", "content": prompt},
        ],
        stream=False,
    )
    return response.choices[0].message.content


def llm_call_openai(msg, model="gpt-4o-mini"):
    # print("backend used openai")
    completion = openai_client.chat.completions.create(
        model=model,
        messages=msg,
    )

    return completion.choices[0].message.content


def llm_call(msg, beackend="openai", model="gpt-4o-mini"):
    if beackend == "openai":
        return llm_call_openai(msg, model)
    elif beackend == "deepseek":
        return llm_call_deepseek(msg)
    else:
        raise ValueError("Invalid backend")
