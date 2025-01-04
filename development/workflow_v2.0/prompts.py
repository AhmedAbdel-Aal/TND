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
- Case Importance
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


def get_citation_aggregation_prompt(facts, law):
    return f"""
Please analyze this case's significance based on its citation analysis data and determine if it constitutes a key case in ECHR jurisprudence.

Consider the following aspects in your analysis:

1. Citation Network Analysis:
- Examine the types of cases being cited (importance levels)
- Analyze the citation types (supportive, distinguishing, etc.)
- Consider the weight given to each citation
- Identify if this case is establishing new principles or mainly relying on existing ones

2. Legal Principles Impact:
- Identify recurring legal principles across citations
- Evaluate if the case expands or refines these principles
- Assess the breadth and importance of legal domains covered
- Determine if the case bridges multiple areas of law

3. Reasoning Patterns:
- Analyze how the case uses precedents
- Evaluate if it creates new legal tests or standards
- Assess if it resolves conflicts between different legal principles
- Consider if it provides clearer guidance than previous cases

4. Citation Context:
- Examine the key similarities and differences patterns
- Evaluate how the case distinguishes or builds upon previous jurisprudence
- Assess if it represents an evolution in legal thinking

Based on the citation analysis provided, please output:

{
    "case_classification": {
        "is_key_case": true/false,
        "classification_score": 1-100,
        "significance_level": "landmark/key/significant/regular",
        "primary_contribution": "main legal contribution",
        "key_factors": [
            "factor1",
            "factor2"
        ]
    },
    "citation_metrics": {
        "total_citations": number,
        "high_importance_citations": number,
        "supportive_citations": number,
        "distinguishing_citations": number
    },
    "legal_impact": {
        "novel_principles": [
            "principle1",
            "principle2"
        ],
        "refined_principles": [
            "principle1",
            "principle2"
        ],
        "scope_of_impact": "narrow/moderate/broad"
    },
    "reasoning": "Detailed explanation of the classification"
}

"""


def get_soc_impact_prompt(facts, law):
    return f"""
Based on the following case details, assess the societal and emotional impact:
- Does the case address issues with significant public interest or controversy? (Yes/No)
- If Yes, describe the societal implications.
- Indicate whether the case is likely to influence future public discourse or policy.

Case Facts:
{facts}

Case Law:
{law}
"""


def get_classify_three_levels_importance_prompt(inputs):
    facts_summary = inputs["facts"]
    law_summary = inputs["law"]
    prompt = f"""
You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.
Your task is to analyze the provided case facts and classify the case into one of the following categories:

1 = High importance: All judgments, decisions and advisory opinions not included in the Case Reports which make a significant contribution to the development, clarification or modification of its case-law, either generally or in relation to a particular State.

2 = Medium importance: Other judgments, decisions and advisory opinions which, while not making a significant contribution to the case-law, nevertheless go beyond merely applying existing case-law.

3 = Low importance: Judgments, decisions and advisory opinions of little legal interest, namely judgments and decisions that simply apply existing case-law, friendly settlements and strike outs (unless raising a particular point of interest).


CASE DETAILS:

Facts:\n{facts_summary}\n\n
Law:\n{law_summary}\n\n

Provide your reasoning step by step, then return your response in the following format:

CLASSIFICATION: [HIGH IMPORTANCE, MEDIUM IMPORTANCE, LOW IMPORTANCE]
REASONING: [Your reasoning for the classification]
"""

    return prompt


def get_classify_key_case_prompt(inputs):
    facts_summary = inputs["facts"]
    law_summary = inputs["law"]
    # importance_analysis = inputs["importance_analysis"]
    citation_analysis = inputs["citation_analysis"]
    prompt = f"""
You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.
A high important case has been identified for further analysis.
Your task is to analyze if the case qualifies as a KEY CASE based on the following criteria:

KEY CASE:
- Makes a significant contribution to the development, clarification, or modification of case law.
- Establishes new legal principles or substantially modifies existing ones.
- Has broad implications beyond the immediate case.

NOT KEY CASE:
- Applies existing case law without significant contributions to legal development.
- Demonstrates limited implications beyond the immediate dispute.



CASE DETAILS:

Facts:\n{facts_summary}\n\n
Law:\n{law_summary}\n\n
Citation Analysis:\n{citation_analysis}\n\n


Provide your reasoning step by step, then return your response in the following format:

CLASSIFICATION: [KEY CASE, NOT KEY CASE]
REASONING: [Your reasoning for the classification]
        """

    return prompt
