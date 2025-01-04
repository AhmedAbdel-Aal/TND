from llm import llm_call


def do_stage_1(articles):
    prompt = f"""
    You are a legal expert specializing in European Court of Human Rights (ECHR) jurisprudence. Your task is to analyze how Convention articles are applied in this case and assess its contribution to ECHR case law.


    Analyze the established legal framework for the articles in question:

    Core Article Analysis:
    For each relevant article ({articles}):
    - List established tests and criteria
    - Identify key principles from landmark cases
    - Note standard interpretations
    - Document typical application contexts

    Example format:
    {{
        "article_baseline": {{
            "article_number": "string",
            "established_tests": [
                {{
                    "test_name": string,
                    "key_elements": [string],
                }}
            ],
            "core_principles": [
                {{
                    "principle": string,
                    "year_established": number
                }}
            ],
            "standard_interpretations": [
                {{
                    "interpretation": string,
                }}
            ]
        }}
    }}
    """

    stage_1 = llm_call(prompt)
    return stage_1


def do_stage_2(case_name, facts, law, stage_1):

    prompt = f"""
    You are a legal expert specializing in European Court of Human Rights (ECHR) jurisprudence. Your task is to analyze how Convention articles are applied in this case and assess its contribution to ECHR case law.

    Analyze how this case applies or deviates from the established framework:

    1. Application Analysis:
    - How does the case use established tests?
    - Are any elements of tests modified?
    - Does it face scenarios not covered by existing principles?

    2. Gap Analysis:
    - What legal questions did the case need to address?
    - Were existing principles sufficient?
    - Where did the case need to develop new approaches?

    1. **Case Details**:
    - Name: {case_name}
    - Facts: {facts}
    - Laws: {law}
    - Baseline Jurisprudence Analysis: {stage_1}


    Example format:
    {{
        "case_analysis": {{
            "application_of_tests": {{
                "test_name": string,
                "standard_application": boolean,
                "modifications": string,
                "reason_for_modification": string
            }},
            "principle_usage": {{
                "principles_applied": [string],
                "gaps_encountered": [string],
                "new_scenarios": [string]
            }}
        }}
    }}
    """

    stage_2 = llm_call(prompt)
    return stage_2


def do_stage_3(case_name, facts, law, citation_analysis, stage_1, stage_2):
    prompt = f"""
    You are a legal expert specializing in European Court of Human Rights (ECHR) jurisprudence. Your task is to assess the novelty of legal elements in this case and identify any true innovations.

    1. For each potentially novel element:
    - Look into the earlier precedents
    - Compare with established principles
    - Evaluate degree of innovation

    1. **Case Details**:
    - Name: {case_name}
    - Facts: {facts}
    - Laws: {law}
    - Citation Analysis: {citation_analysis}
    - Baseline Jurisprudence Analysis: {stage_1}
    - Case-Specific Analysis and Gap Identification: {stage_2}


    Output format:
    {{
        "novelty_assessment": {{
            "claimed_novelties": [
                {{
                    "element": string,
                    "claimed_as": string,
                    "validation": {{
                        "is_truly_novel": boolean,
                        "earlier_precedents": [string],
                        "reasoning": string
                    }}
                }}
            ]
        }}
    }}

    Remember:
    - Be skeptical of novelty claims
    - Search thoroughly for precedents
    - Distinguish between true innovation and application
    - Consider the full body of ECHR case law
    """

    stage_3 = llm_call(prompt)
    return stage_3


def get_probabilities(
    case_name, facts, law, citation_analysis, stage_1, stage_2, stage_3
):
    prompt = f"""
    You are a legal expert specializing in ECHR jurisprudence. Your task is to determine whether this case qualifies as a key case by synthesizing multiple layers of analysis.

    ### Key Case Definition:
    A "Key Case" is one that:
    1. Establishes new legal principles or significantly redefines existing ones.
    2. Resolves critical gaps or ambiguities in ECHR jurisprudence.
    3. Has broad implications beyond the immediate case, influencing policy, legal frameworks, or societal standards.
    4. Addresses systemic or unprecedented legal challenges, setting a precedent for future cases.

    ### **Not Key Case Definition**:
    A "Not Key Case" is one that:
    1. Applies existing legal principles without introducing significant new interpretations.
    2. Primarily addresses specific factual circumstances without broader implications.
    3. Resolves issues that are procedural or technical in nature rather than substantive.
    4. Demonstrates limited impact beyond the immediate dispute, lacking systemic or jurisprudential influence.

    ### CASE INFORMATION:
    - Case Name: {case_name}
    - Facts: {facts}
    - Law: {law}
    - Citation Analysis: {citation_analysis}
    - Baseline Jurisprudence Analysis: {stage_1}
    - Case-Specific Analysis and Gap Identification: {stage_2}
    - Novelty Assessment: {stage_3}

    ### Analysis Instructions:

    1. **Analyze and Argue**:
    - Provide a detailed argument for why the case might qualify as a "Key Case."
    - Provide a detailed argument for why the case might qualify as a "Not Key Case."

    2. **Assign Probabilities**:
    - Based on your analysis, assign probabilities to each classification:
        - Probability of "Key Case."
        - Probability of "Not Key Case."

    ### **Expected Output (in JSON Format)**:

    {{
        "arguments": {{
            "Key Case": "Detailed reasoning for why the case might qualify as a Key Case",
            "Not Key Case": "Detailed reasoning for why the case might qualify as NOT a Key Case"
        }},
        "probabilities": {{
            "Key Case": "Probability (%)",
            "Not Key Case": "Probability (%)"
        }}
    }}

    Remember:
    1. Think step by step, use the provided case information and analyses.
    2. Consider the novelty assessment and gap analysis.
    3. Cross-reference all provided analyses
    4. Consider both immediate and long-term effects
    5. Evaluate geographic and temporal scope
    6. Assess practical implementation requirements

    Let's think step by step:
    """

    response = llm_call(prompt)
    return response
