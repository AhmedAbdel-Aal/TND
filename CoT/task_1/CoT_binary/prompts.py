from langchain.prompts import PromptTemplate


def get_CoT_facts_prompt(facts):
    return f"""
You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.
Your task is to analyze the provided case facts and classify the case into one of the following categories:

KEY CASE:
- Makes a significant contribution to the development, clarification, or modification of case law.
- Establishes new legal principles or substantially modifies existing ones.
- Has broad implications beyond the immediate case.

NOT KEY CASE:
- Applies existing case law without significant contributions to legal development.
- Demonstrates limited implications beyond the immediate dispute.

Case Facts:
{facts}

Provide your reasoning step by step and conclude with one of the following exact classifications:

Return your response in this format:
EXPLANATION: [Your space to think step by step about the task, and self reflect on your reasoning]
CLASSIFICATION: [KEY CASE, NOT KEY CASE]
REASONING: [THE ONE LINE WITH THE EXACT REASON FOR THE CLASSIFICATION]
"""


def get_CoT_law_prompt(law):
    return f"""
You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.
Your task is to analyze the provided case law section and classify the case into one of the following categories:

KEY CASE:
- Makes a significant contribution to the development, clarification, or modification of case law.
- Establishes new legal principles or substantially modifies existing ones.
- Has broad implications beyond the immediate case.

NOT KEY CASE:
- Applies existing case law without significant contributions to legal development.
- Demonstrates limited implications beyond the immediate dispute.

Case Law Section:
{law}

Provide your reasoning step by step and conclude with one of the following exact classifications:

Return your response in this format:
EXPLANATION: [Your space to think step by step about the task, and self reflect on your reasoning]
CLASSIFICATION: [KEY CASE, NOT KEY CASE]
REASONING: [THE ONE LINE WITH THE EXACT REASON FOR THE CLASSIFICATION]
"""


def get_CoT_facts_law_prompt(facts, law):
    return f"""
You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.
Your task is to analyze the provided case facts and law sections, then classify the case into one of the following categorie:

KEY CASE:
- Makes a significant contribution to the development, clarification, or modification of case law.
- Establishes new legal principles or substantially modifies existing ones.
- Has broad implications beyond the immediate case.

NOT KEY CASE:
- Applies existing case law without significant contributions to legal development.
- Demonstrates limited implications beyond the immediate dispute.

Case Facts:
{facts}

Case Law Section:
{law}

Provide your reasoning step by step and conclude with one of the following exact classifications:

Return your response in this format:
EXPLANATION: [Your space to think step by step about the task, and self reflect on your reasoning]
CLASSIFICATION: [KEY CASE, NOT KEY CASE]
REASONING: [THE ONE LINE WITH THE EXACT REASON FOR THE CLASSIFICATION]
"""
