def get_summarize_facts_prompt(facts):
    return f"Summarize the following legal case facts:\n{facts}"


def get_summarize_law_prompt(law):
    return f"Summarize the following legal case law:\n{law}"


def get_extract_legal_principles_prompt(facts):
    return f"""
Analyze these case facts and provide:

KEY LEGAL PRINCIPLES:
- Extract the main legal principles discussed or applied
- Show how each principle relates to specific ECHR Articles
- Note any conflicts or balancing between principles

Please provide a structured analysis that clearly maps principles to Articles.

case facts:\n{facts}
"""


def get_citation_analysis_prompt(facts, law):
    return f"""
Analyze these case facts and law sections and provide:


1. CHRONOLOGICAL CASE LIST:
For each cited case, provide:
- Full case name
- Date
- Analyze WHY this case was cited. For example:
    - Similar factual circumstances
    - Previous legal reasoning being applied
    - Established principles being referenced
    - Procedural precedents
    - Other reasons
- Analyze HOW this case was cited. For example:
    - Direct application of precedent
    - Extension of previous principles
    - Distinguishing from previous case
    - Clarifying previous interpretation
    - Other approaches

Case Facts:
{facts}

Case Law:
{law}

Cited ECHR Cases:
"""


def get_classify_key_case_prompt(inputs):
    facts_summary = inputs["facts_summary"]
    law_summary = inputs["law_summary"]
    legal_principles = inputs["legal_principles"]
    citation_analysis = inputs["citation_analysis"]
    prompt = f"""
You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.
Your task is to analyze the provided case facts and classify the case into one of the following categories:

KEY CASE:
- Makes a significant contribution to the development, clarification, or modification of case law.
- Establishes new legal principles or substantially modifies existing ones.
- Has broad implications beyond the immediate case.

NOT KEY CASE:
- Applies existing case law without significant contributions to legal development.
- Demonstrates limited implications beyond the immediate dispute.

INPUTS:

Facts Summary:\n{facts_summary}\n\n
Law Summary:\n{law_summary}\n\n
Legal Principles and Articles:\n{legal_principles}\n\n
Citation Analysis:\n{citation_analysis}

Provide your reasoning step by step, then return your response in the following format:

CLASSIFICATION: [KEY CASE, NOT KEY CASE]
REASONING: [Your reasoning for the classification]
        """

    return prompt


def get_classify_key_case_prompt_workflow_4(inputs):
    facts_summary = inputs["facts_summary"]
    law_summary = inputs["law_summary"]
    legal_principles = inputs["legal_principles"]
    citation_analysis = inputs["citation_analysis"]
    prompt = f"""
You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.

Classify the following ECHR case into one of two categories: **"KEY CASE"** or **"NOT KEY CASE,"** based on the case's legal and societal impact, contribution to case law, and novelty.

CLASSIFICATION CATEGORIES:

1. KEY CASE
   - Definition: Cases that have significant legal and societal implications, set important precedents, introduce new legal principles, or address novel and complex issues within the context of human rights law.
   - Indicators:
     - Legal Impact: Introduces or significantly alters legal principles or interpretations.
     - Societal Impact: Influences societal norms, policies, or practices on a broad scale.
     - Contribution to Case Law: Sets a precedent, guides future cases, or provides substantial clarification within its legal context.
     - Novelty: Addresses unprecedented legal questions or applies existing principles in a notably new manner.

2. NOT KEY CASE
   - Definition: Cases that apply established legal principles without significant development, focus on procedural matters, or have limited societal implications.
   - Indicators:
     - Legal Impact: Applies existing legal principles without significant alteration.
     - Societal Impact: Minimal influence on societal norms or policies.
     - Contribution to Case Law: Limited or no precedent-setting; mostly reiterates existing jurisprudence.
     - Novelty: Deals with routine or well-established legal issues without introducing new perspectives.


INSTRUCTIONS
1. Analyze the Case Details: Review the provided case facts, legal issues, and any given analysis.
2. Evaluate Based on Criteria: Assess the case's impact, contribution, and novelty using the outlined indicators for each category.
3. Assign the Appropriate Classification: Determine whether the case fits **"KEY CASE"** or **"NOT KEY CASE"** based on your evaluation.
4. Provide Justification: Offer a clear and concise explanation for your classification, referencing specific aspects of the case that align with the category definitions.


INPUTS:
Facts:\n{facts_summary}\n\n
Law:\n{law_summary}\n\n
Legal Principles and Articles:\n{legal_principles}\n\n
Citation Analysis:\n{citation_analysis}


RESPONSE FORMAT:

Provide your reasoning step by step, then return your response in the following format:

CLASSIFICATION: [KEY CASE, NOT KEY CASE]
REASONING: [Your reasoning for the classification]
"""

    return prompt


def get_classify_three_levels_importance_prompt(inputs):
    facts_summary = inputs["facts_summary"]
    law_summary = inputs["law_summary"]
    legal_principles = inputs["legal_principles"]
    citation_analysis = inputs["citation_analysis"]
    prompt = f"""
You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.
Your task is to analyze the provided case facts and classify the case into one of the following categories:

HIGH IMPORTANCE:
- Makes a significant contribution to the development, clarification, or modification of case law.
- Establishes new legal principles or substantially modifies existing ones.

MEDIUM IMPORTANCE:
- Not making a significant contribution, but go beyond merely applying existing case-law

LOW IMPORTANCE:
- Applies existing case law without significant contributions to legal development.
- Demonstrates limited implications beyond the immediate dispute.


INPUTS:

Facts Summary:\n{facts_summary}\n\n
Law Summary:\n{law_summary}\n\n
Legal Principles and Articles:\n{legal_principles}\n\n
Citation Analysis:\n{citation_analysis}

Provide your reasoning step by step, then return your response in the following format:

CLASSIFICATION: [HIGH IMPORTANCE, MEDIUM IMPORTANCE, LOW IMPORTANCE]
REASONING: [Your reasoning for the classification]
"""

    return prompt


def get_classify_three_levels_importance_prompt_workflow_4(inputs):
    facts_summary = inputs["facts_summary"]
    law_summary = inputs["law_summary"]
    legal_principles = inputs["legal_principles"]
    citation_analysis = inputs["citation_analysis"]
    prompt = f"""
You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.

Your task is to classify the following ECHR case into one of three levels of importance [HIGH IMPORTANCE, MEDIUM IMPORTANCE, LOW IMPORTANCE] based on the case's legal and societal impact, contribution to case law, and novelty.

CLASSIFICATION CATEGORIES:

- HIGH IMPORTANCE: Reserved for the most significant judgments, decisions, and advisory opinions selected for their substantial legal and societal impact. These cases often set landmark precedents or introduce significant developments in legal principles or their interpretation. They shape jurisprudence in transformative ways that extend across jurisdictions or legal systems.

- MEDIUM IMPORTANCE: Comprises judgments, decisions, and advisory opinions that go beyond merely applying existing case law but do not make a significant contribution to its development or clarification. These cases may highlight procedural nuances or reiterate established principles, with limited systemic or societal impact

- LOW IMPORTANCE: Routine Cases with Limited Impact Comprises cases that apply established principles without significant development, focus on procedural nuances, or have minimal societal implications.

INSTRUCTIONS
1. Analyze the Case Details: Review the provided case facts, legal issues, and any given analysis.
2. Evaluate Based on Criteria: Assess the case's impact, contribution, and novelty using the outlined indicators for each category.
3. Assign the Appropriate Classification: Determine whether the case fits **"KEY CASE"** or **"NOT KEY CASE"** based on your evaluation.
4. Provide Justification: Offer a clear and concise explanation for your classification, referencing specific aspects of the case that align with the category definitions.


INPUTS:
Facts:\n{facts_summary}\n\n
Law:\n{law_summary}\n\n
Legal Principles and Articles:\n{legal_principles}\n\n
Citation Analysis:\n{citation_analysis}


RESPONSE FORMAT:

Provide your reasoning step by step, then return your response in the following format:

CLASSIFICATION: [HIGH IMPORTANCE, MEDIUM IMPORTANCE, LOW IMPORTANCE]
REASONING: [Your reasoning for the classification]
"""

    return prompt


def get_classify_four_levels_importance_prompt(inputs):
    facts_summary = inputs["facts_summary"]
    law_summary = inputs["law_summary"]
    legal_principles = inputs["legal_principles"]
    citation_analysis = inputs["citation_analysis"]
    prompt = f"""
You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.
Your task is to analyze the provided case facts and classify the case into one of the following categories:

LEVEL 1:
- Reserved for the most significant judgments, decisions, and advisory opinions selected for their substantial legal and societal impact.
- These cases often set landmark precedents or introduce significant developments in legal principles or their interpretation.
- They shape jurisprudence in transformative ways that extend across jurisdictions or legal systems.
- Makes a significant contribution to the development, clarification, or modification of case law.
- Establishes new legal principles or substantially modifies existing ones.
- Has broad implications beyond the immediate case.

LEVEL 2:
- Includes judgments, decisions, and advisory opinions that are not landmark cases but make a significant contribution to developing or clarifying case law.
- These cases may address key issues or refine principles within specific contexts or areas of law, influencing but not overhauling broader jurisprudence.

LEVEL 3:
- Comprises judgments, decisions, and advisory opinions that go beyond merely applying existing case law but do not make a significant contribution to its development or clarification.
- These cases may highlight procedural nuances or reiterate established principles, with limited systemic or societal impact

LEVEL 4:
- Comprises Judgments, decisions, and advisory opinions of little legal interest, such as those that simply apply existing case-law, friendly settlements, and strikeouts.
- Applies existing case law without significant contributions to legal development.
- Demonstrates limited implications beyond the immediate dispute.


INPUTS:

Facts:\n{facts_summary}\n\n
Law:\n{law_summary}\n\n
Legal Principles and Articles:\n{legal_principles}\n\n
Citation Analysis:\n{citation_analysis}


RESPONSE FORMAT:

Provide your reasoning step by step, then return your response in the following format:

CLASSIFICATION: [LEVEL 1, LEVEL 2, LEVEL 3, LEVEL 4]
REASONING: [Your reasoning for the classification]
"""

    return prompt


def get_classify_four_levels_importance_prompt_workflow_4(inputs):
    facts_summary = inputs["facts_summary"]
    law_summary = inputs["law_summary"]
    legal_principles = inputs["legal_principles"]
    citation_analysis = inputs["citation_analysis"]
    prompt = f"""
You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.

Your task is to classify the following ECHR case into one of four levels of importance [LEVEL 1, LEVEL 2, LEVEL 3, LEVEL 4] based on the case's legal and societal impact, contribution to case law, and novelty.

CLASSIFICATION CATEGORIES:

- LEVEL 1: Reserved for the most significant judgments, decisions, and advisory opinions selected for their substantial legal and societal impact. These cases often set landmark precedents or introduce significant developments in legal principles or their interpretation. They shape jurisprudence in transformative ways that extend across jurisdictions or legal systems.

- LEVEL 2: Includes judgments, decisions, and advisory opinions that are not landmark cases but make a significant contribution to developing or clarifying case law. These cases may address key issues or refine principles within specific contexts or areas of law, influencing but not overhauling broader jurisprudence.

- LEVEL 3: Comprises judgments, decisions, and advisory opinions that go beyond merely applying existing case law but do not make a significant contribution to its development or clarification. These cases may highlight procedural nuances or reiterate established principles, with limited systemic or societal impact

- LEVEL 4: Comprises Judgments, decisions, and advisory opinions of little legal interest, such as those that simply apply existing case-law, friendly settlements, and strikeouts.



INSTRUCTIONS
1. Analyze the Case Details: Review the provided case facts, legal issues, and any given analysis.
2. Evaluate Based on Criteria: Assess the case's impact, contribution, and novelty using the outlined indicators for each category.
3. Assign the Appropriate Classification: Determine whether the case fits **"KEY CASE"** or **"NOT KEY CASE"** based on your evaluation.
4. Provide Justification: Offer a clear and concise explanation for your classification, referencing specific aspects of the case that align with the category definitions.


INPUTS:
Facts:\n{facts_summary}\n\n
Law:\n{law_summary}\n\n
Legal Principles and Articles:\n{legal_principles}\n\n
Citation Analysis:\n{citation_analysis}


RESPONSE FORMAT:

Provide your reasoning step by step, then return your response in the following format:

CLASSIFICATION: [LEVEL 1, LEVEL 2, LEVEL 3, LEVEL 4]
REASONING: [Your reasoning for the classification]
"""

    return prompt
