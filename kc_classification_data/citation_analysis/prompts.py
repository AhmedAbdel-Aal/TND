def get_summarizer_prompt(text: str) -> str:
    return f"""
You are a specialist in European Court of Human Rights (ECHR) jurisprudence.
Your task is to provide a summary of the given legal case, including all key points and supporting details.
The summary should be comprehensive and accurately reflect the main and most important facts, procedure, and arguments presented in the original text,
while also being concise and easy to understand. To ensure accuracy, please read the text carefully and pay attention to any nuances or complexities in the language.

Do not provide any explanations or text apart from the summary.

case:
{text}

Summary:
"""


def get_analysis_prompt(case_A: str, case_B: str) -> str:
    return f"""
You are a specialist in European Court of Human Rights (ECHR) jurisprudence.
Knowing that case A cited case B. Your task is to analyze the connection between case A and case B.
What legal principles or facts from Case B does Case A rely on? Does Case A use Case B as precedent, analogy, or to highlight a contrasting viewpoint?

Case A Summary:
{case_A}

Case B Summary:
{case_B}

Analysis:
"""
