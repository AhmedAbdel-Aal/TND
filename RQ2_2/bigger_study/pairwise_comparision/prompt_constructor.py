prompt = """
Please act as an impartial judge and evaluate the quality of the responses provided by two
AI assistants to the user question displayed below:
    - read the actual facts, conclusion of the case.
    - read the generated reasoning of the two AI assistants.
    - compare the generated reasoning of the two AI assistants with the actual law section
    - Give a score between 1 and 5 for each of the checklist question and explain your scores for each AI assistants.

[The evaluation questions]
    1. Main elements of the precedents/legal notion (identification of articles)
    2. Identification of factual circumstances
    3. Explanation of the connection between legal notions and factual circumstances
    4. Explanation of the recurrence/divergence of the circumstances from the main precedents
    5. Grounding facts in correct legal precedence

After providing your explanation, output your final verdict by strictly following this format: "[[A]]" if assistant A is better, "[[B]]" if assistant B is better, and "[[C]]" for a tie.

[The start of the actual case]
{case}
[The end of the actual case]

[The Start of Assistant A’s Answer]
{answer_A}
[The End of Assistant A’s Answer]

[The Start of Assistant B’s Answer]
{answer_B}
[The End of Assistant B’s Answer]
"""
