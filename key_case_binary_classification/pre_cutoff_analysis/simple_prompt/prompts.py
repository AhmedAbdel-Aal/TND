from langchain.prompts import PromptTemplate


def get_prompt(prompt_id, **kwargs):
    if prompt_id == "1":
        return get_simple_CoT_facts_prompt(**kwargs)
    elif prompt_id == "2":
        return get_simple_CoT_facts_law_prompt(**kwargs)
    elif prompt_id == "3":
        return gpt_CoT_facts_prompt(**kwargs)
    elif prompt_id == "4":
        return gpt_CoT_facts_prompt_2(**kwargs)


def get_simple_CoT_facts_prompt(**kwargs):
    return PromptTemplate(
        input_variables=["case_facts"],
        template="""
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
            {case_facts}

            Provide your reasoning step by step and conclude with one of the following exact classifications:

            CLASSIFICATION: KEY CASE
            CLASSIFICATION: NOT KEY CASE
        """,
    )


def get_simple_CoT_facts_law_prompt(**kwargs):
    return PromptTemplate(
        input_variables=["case_facts", "law"],
        template="""
            You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.
            Your task is to analyze the provided case facts and law section, then classify the case into one of the following categories::

            KEY CASE:
            - Makes a significant contribution to the development, clarification, or modification of case law.
            - Establishes new legal principles or substantially modifies existing ones.
            - Has broad implications beyond the immediate case.

            NOT KEY CASE:
            - Applies existing case law without significant contributions to legal development.
            - Demonstrates limited implications beyond the immediate dispute.

            Case Facts:
            {case_facts}

            Case Law Section:
            {law}

            Provide your reasoning step by step and conclude with one of the following exact classifications:

            CLASSIFICATION: KEY CASE
            CLASSIFICATION: NOT KEY CASE
        """,
    )


def gpt_CoT_facts_prompt(**kwargs):
    return PromptTemplate(
        input_variables=["case_facts"],
        template="""
Instruction:
You are a highly skilled legal analyst tasked with classifying legal cases into two categories based on their facts section:

    - Key Case: A case with substantial legal importance, such as setting a significant precedent, resolving major legal ambiguities, or influencing future cases.
    - Non-Key Case: A case that deals with routine matters, applies established principles, or lacks broader legal implications.

Follow these steps to ensure accurate classification:

    - Understand the Facts: Identify the essential details, focusing on the legal issues and outcomes.
    - Assess Significance: Consider whether the case introduces new interpretations, resolves conflicts, or sets a precedent.
    - Contextualize: Compare the case's significance against common legal benchmarks for precedent and broader impact.
    - Justify Classification: Provide a clear, step-by-step rationale for your decision.
    - Self-Check: Reevaluate the classification by reviewing the facts and reasoning for consistency.

Examples for Guidance:

Example 1:

Facts:
A Supreme Court case resolves a longstanding conflict between state and federal regulations regarding environmental protection. The ruling creates a new standard for federal preemption and influences future cases nationwide.

Reasoning:

    The case resolves a critical legal conflict (state vs. federal regulations).
    It establishes a new standard, setting a significant precedent.
    The decision has implications beyond the immediate dispute, affecting future cases nationwide.

Classification: Key Case.

Example 2:

Facts:
A local court case dismisses a claim because it lacks sufficient evidence to proceed to trial. The ruling applies well-established evidentiary standards without introducing new interpretations.

Reasoning:

    The case applies existing legal principles (evidentiary standards).
    It does not introduce new interpretations or broader legal implications.
    The outcome is routine and lacks precedent-setting value.

Classification: Non-Key Case.

Case for Classification:

Facts:
{case_facts}

Step-by-Step Reasoning:

    Understand the Facts: What are the key issues, outcomes, and legal principles involved?
    Assess Significance: Does the case resolve ambiguities, set new precedents, or influence future cases?
    Contextualize: Compare its significance to typical key cases.
    Justify Classification: Explain your decision step by step.
    Self-Check: Reassess the reasoning and ensure alignment with the classification criteria.

Classification: [Key Case/Non-Key Case]
""",
    )


def gpt_CoT_facts_prompt_2(**kwargs):
    return PromptTemplate(
        input_variables=["case_facts"],
        template="""
You are a legal analyst specializing in European Court of Human Rights (ECHR) jurisprudence tasked with determining whether a legal case is a key case or a non-key case based on its facts.

A Key Case is one that:
    - Resolves significant legal ambiguities.
    - Sets a new legal precedent.
    - Has a broad impact on future cases or legal principles.

A Non-Key Case is one that:
    - Applies existing principles without introducing new interpretations.
    - Addresses routine or procedural matters.
    - Lacks broader implications for the legal system.

Task:
Based on the facts provided, classify the case as either a Key Case or a Non-Key Case. Your decision should be based strictly on the criteria above.

Facts:
{case_facts}

Classification: [Key Case/Non-Key Case]

""",
    )
