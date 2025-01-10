from langchain.prompts import PromptTemplate


def get_CoT_facts_prompt(facts):
    return f"""
You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.
Your task is to analyze the provided case facts and classify the case into one of the following categories:

LEVEL 1:
- Judgments, decisions and advisory opinions which make a significant contribution to the development, clarification or modification of its case-law, either generally or in relation to a particular State.

LEVEL 2:
- Judgments, decisions and advisory opinions which, while not making a significant contribution to the case-law, nevertheless go beyond merely applying existing case-law.

LEVEL 3:
- Judgments, decisions and advisory opinions of little legal interest, namely judgments and decisions that simply apply existing case-law, friendly settlements and strike outs (unless raising a particular point of interest).


Case Facts:
{facts}

Provide your reasoning step by step and conclude with one of the following exact classifications:

Return your response in this format:
EXPLANATION: [Your space to think step by step about the task, and self reflect on your reasoning]
CLASSIFICATION: [LEVEL 1, LEVEL 2, LEVEL 3]
REASONING: [THE ONE LINE WITH THE EXACT REASON FOR THE CLASSIFICATION]
"""


def get_CoT_law_prompt(law):
    return f"""
You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.
Your task is to analyze the provided case law section and classify the case into one of the following categories:

LEVEL 1:
- Judgments, decisions and advisory opinions which make a significant contribution to the development, clarification or modification of its case-law, either generally or in relation to a particular State.

LEVEL 2:
- Judgments, decisions and advisory opinions which, while not making a significant contribution to the case-law, nevertheless go beyond merely applying existing case-law.

LEVEL 3:
- Judgments, decisions and advisory opinions of little legal interest, namely judgments and decisions that simply apply existing case-law, friendly settlements and strike outs (unless raising a particular point of interest).

Case Law Section:
{law}

Provide your reasoning step by step and conclude with one of the following exact classifications:

Return your response in this format:
EXPLANATION: [Your space to think step by step about the task, and self reflect on your reasoning]
CLASSIFICATION: [LEVEL 1, LEVEL 2, LEVEL 3]
REASONING: [THE ONE LINE WITH THE EXACT REASON FOR THE CLASSIFICATION]
"""


def get_CoT_facts_law_prompt(facts, law):
    return f"""
You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.
Your task is to analyze the provided case facts and law sections, then classify the case into one of the following categorie:

LEVEL 1:
- Judgments, decisions and advisory opinions which make a significant contribution to the development, clarification or modification of its case-law, either generally or in relation to a particular State.

LEVEL 2:
- Judgments, decisions and advisory opinions which, while not making a significant contribution to the case-law, nevertheless go beyond merely applying existing case-law.

LEVEL 3:
- Judgments, decisions and advisory opinions of little legal interest, namely judgments and decisions that simply apply existing case-law, friendly settlements and strike outs (unless raising a particular point of interest).

Case Facts:
{facts}

Case Law Section:
{law}

Provide your reasoning step by step and conclude with one of the following exact classifications:

Return your response in this format:
EXPLANATION: [Your space to think step by step about the task, and self reflect on your reasoning]
CLASSIFICATION: [LEVEL 1, LEVEL 2, LEVEL 3]
REASONING: [THE ONE LINE WITH THE EXACT REASON FOR THE CLASSIFICATION]
"""
