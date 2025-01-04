from openai import OpenAI
from typing import Dict
from prompts import get_CoT_facts_prompt, get_CoT_law_prompt, get_CoT_facts_law_prompt


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


def cot_facts(facts):
    response = llm_call_openai(get_CoT_facts_prompt(facts))
    return response


def cot_law(law):
    response = llm_call_openai(get_CoT_law_prompt(law))
    return response


def cot_facts_law(facts, law):
    response = llm_call_openai(get_CoT_facts_law_prompt(facts, law))
    return response
