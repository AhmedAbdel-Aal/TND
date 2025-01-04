from langchain.prompts import PromptTemplate


def get_prompt(prompt_id, **kwargs):
    if prompt_id == "1":
        return get_simple_CoT_facts_prompt(**kwargs)
    elif prompt_id == "2":
        return get_simple_CoT_facts_law_prompt(**kwargs)


def get_simple_CoT_facts_prompt(**kwargs):
    return PromptTemplate(
        input_variables=["case_facts"],
        template="""
You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.
Your task is to analyze the provided case facts and classify the case importance into one of the following categories:

1 = High importance: All judgments, decisions and advisory opinions not included in the Case Reports which make a significant contribution to the development, clarification or modification of its case-law, either generally or in relation to a particular State.

2 = Medium importance: Other judgments, decisions and advisory opinions which, while not making a significant contribution to the case-law, nevertheless go beyond merely applying existing case-law.

3 = Low importance: Judgments, decisions and advisory opinions of little legal interest, namely judgments and decisions that simply apply existing case-law, friendly settlements and strike outs (unless raising a particular point of interest).

Case Facts:
{case_facts}

Provide your reasoning step by step and conclude with one of the following exact classifications:

CLASSIFICATION: [HIGH IMPORTANCE, MEDIUM IMPORTANCE, LOW IMPORTANCE]
REASONING: [Your reasoning for the classification]
        """,
    )


def get_simple_CoT_facts_law_prompt(**kwargs):
    return PromptTemplate(
        input_variables=["case_facts", "law"],
        template="""
You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.
Your task is to analyze the provided case facts and law sections, then classify the case importance into one of the following categories:

1 = High importance: All judgments, decisions and advisory opinions not included in the Case Reports which make a significant contribution to the development, clarification or modification of its case-law, either generally or in relation to a particular State.

2 = Medium importance: Other judgments, decisions and advisory opinions which, while not making a significant contribution to the case-law, nevertheless go beyond merely applying existing case-law.

3 = Low importance: Judgments, decisions and advisory opinions of little legal interest, namely judgments and decisions that simply apply existing case-law, friendly settlements and strike outs (unless raising a particular point of interest).

Case Facts:
{case_facts}

Case Law Section:
{law}

Provide your reasoning step by step and conclude with one of the following exact classifications:

CLASSIFICATION: [HIGH IMPORTANCE, MEDIUM IMPORTANCE, LOW IMPORTANCE]
REASONING: [Your reasoning for the classification]
        """,
    )
