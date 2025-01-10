from openai import OpenAI
from typing import Dict
from prompts import get_CoT_facts_prompt, get_CoT_law_prompt, get_CoT_facts_law_prompt
import dotenv

dotenv.load_dotenv()


def llm_call_deepseek(prompt):

    client = OpenAI(
        api_key=os.environ["DEEP_SEEK"], base_url="https://api.deepseek.com"
    )
    response = client.chat.completions.create(
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


def llm_call_openai(prompt, model="gpt-4o-mini"):
    client = OpenAI()

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return completion.choices[0].message.content


def llm_call(prompt, beackend="deepseek", model="gpt-4o-mini"):
    if beackend == "openai":
        return llm_call_openai(prompt, model)
    elif beackend == "deepseek":
        return llm_call_deepseek(prompt)
    else:
        raise ValueError("Invalid backend")


def cot_facts(facts):
    response = llm_call_openai(get_CoT_facts_prompt(facts))
    return response


def cot_law(law):
    response = llm_call_openai(get_CoT_law_prompt(law))
    return response


def cot_facts_law(facts, law):
    response = llm_call_openai(get_CoT_facts_law_prompt(facts, law))
    return response
