import re
import os
import json
from tqdm import tqdm
from .utils import llm_call, extract_paragraphs_from_list
from .utils import load_json, save_json, normalize, find_closest_match
import tiktoken

paragraph_num_re = re.compile(r"^(\d+)\.\s*(.*)$")

citation_pattern = re.compile(
    r"""
    # Optional leading punctuation or "see ...", e.g. "(see ...", "[see ..."
    (?P<leading_punct>
        [\(\[]?                          # possibly "(" or "["
        (?:see(?:\s+in\sparticular)?\s+)?  # optionally "see" or "see in particular"
    )?

    # Case name
    (?P<case_name>
        [A-Z][^,\(\)\[\]]*              # 1) First side: starts uppercase, then anything except comma/()[]
        \s+v\.?\s+                      # " v. " or " v " or " v."
        [a-zA-Z][^,\(\)\[]*             # 2) Second side: allow uppercase or lowercase (for "the"), continuing
    )

    # Possibly something like " [GC]" or " [Committee]" or bracketed content
    (?P<parenthetical>
        (?:\s*\[[^\]]+\])?
    )?

    # Optional footnote digits right after bracketed content
    (?P<footnote>
        (?:\d+)?
    )

    # Optional comma
    (?:,\s*)?

    # Application numbers: "nos. 66069/09 and 2 others", "no. 31250/02"
    (?P<application_numbers>
        (?:no\.|nos\.)
        [^,§]+
    )?

    # Optional comma
    (?:,\s*)?

    # Paragraph references: "§ 27", "§§ 124-30", etc.
    (?P<paragraphs>
        §§?.*?\d+
        (?:,\s?\d+)?
        (?:[-–]\d+)?
        (?:\s*(?:and|,)\s*§§?\d+(?:[-–]\d+)?)*
    )?

    # Optional comma
    (?:,\s*)?

    # Date: e.g. "ECHR 2013", "17 January 2023", "ECHR 2013 (extracts)"
    # Some references have "ECHR 2013" or "ECHR 2013 (extracts)" instead of a day-month-year date.
    # If you want to capture that, you might do:
    (?P<date>
        (?:\d{1,2}\s+[A-Z][a-z]+\s+\d{4})          # day-month-year
        |
        (?:ECHR\s+\d{4}(?:\s*\(extracts\))?)       # e.g. "ECHR 2013" or "ECHR 2013 (extracts)"
    )?

    # Optional trailing punctuation, e.g. ")" or "]"
    (?P<trailing_punct>
        [\)\]]?
    )?
    """,
    re.VERBOSE,
)


def fix_paragraphs(paragraphs_string: str) -> str:
    """
    Insert a dash if we have something like '§§ 6873' => '§§ 68-73'.
    """
    if not paragraphs_string:
        return ""

    # Insert dash between 4 digits if we see e.g. "§§ 6873"
    pattern_missing_dash = re.compile(r"(§§?\s*)(\d{2})(\d{2})\b")

    def insert_dash(m):
        return f"{m.group(1)}{m.group(2)}-{m.group(3)}"

    paragraphs_fixed = pattern_missing_dash.sub(insert_dash, paragraphs_string)
    return paragraphs_fixed.strip()


def expand_editorial_shortening(start_par: int, end_par: int) -> int:
    """
    If end_par < start_par, handle the editorial style "§§ 115-31" => (115, 131).
    """
    if end_par >= start_par:
        return end_par

    # E.g. start_par=115, end_par=31 => "115" and "31"
    s_start = str(start_par)
    s_end = str(end_par)

    diff = len(s_start) - len(s_end)
    if diff <= 0:
        return end_par

    # e.g. s_start="115", s_end="31" => prefix="1" => "1"+"31" => 131
    prefix = s_start[: -len(s_end)]
    new_str = prefix + s_end
    try:
        new_end = int(new_str)
        if new_end < start_par:
            # Possibly we have to do more, but typically once is enough
            pass
        return new_end
    except ValueError:
        return end_par


def parse_paragraph_range(paragraphs_string: str) -> (int, int):
    """
    Extract the numeric range from the first chunk if multiple references.

    e.g. "§§ 124-30" => (124, 130)
         "§ 200" => (200, 200)
         "§§ 115-31" => (115, 131) after editorial expansion
    """
    if not paragraphs_string:
        return (None, None)

    fixed_string = fix_paragraphs(paragraphs_string)

    # Split on commas or "and" to handle multiple references, but parse only the first chunk
    references = re.split(r",\s*|\sand\s+", fixed_string)
    if not references:
        return (None, None)
    first_chunk = references[0].strip()

    # remove '§' or '§§' etc.
    step1 = re.sub(r"§+", "", first_chunk)
    # keep only digits and dashes
    chunk_clean = re.sub(r"[^\d-]", "", step1)

    if "-" in chunk_clean:
        # e.g. "124-30"
        parts = chunk_clean.split("-", 1)
        if len(parts) == 2:
            try:
                start_par = int(parts[0])
            except ValueError:
                return (None, None)
            try:
                end_par = int(parts[1])
            except ValueError:
                return (start_par, None)

            if end_par < start_par:
                end_par = expand_editorial_shortening(start_par, end_par)

            return (start_par, end_par)
        else:
            return (None, None)
    else:
        # single number => (val, val)
        try:
            val = int(chunk_clean)
            return (val, val)
        except ValueError:
            return (None, None)


def extract_echr_citations(law_paragraphs):
    """
    law_paragraphs: list of paragraph texts (some with a leading "37. ").
    Returns: a list of dicts with:
        {
          'paragraph': '37',  # or None
          'citation': {
            'full_citation': the entire matched string,
            'case_name': 'Vinter and Others v. the United Kingdom',
            'parenthetical': '[GC]',
            'committee': None,  # or 'Committee'
            'footnote': None,   # or footnote digits
            'application_numbers': 'nos. 66069/09 and 2 others',
            'paragraphs': '§§ 124-30',
            'start_paragraph_ref': 124,
            'end_paragraph_ref': 130,
            'date': 'ECHR 2013 (extracts)',  # or '17 January 2023'
            'start': <match start in string>,
            'end': <match end in string>
          }
        }
    """
    all_citations = []

    for para_text in law_paragraphs:
        # Extract paragraph number if it starts with e.g. "37."
        paragraph_number = None
        match_parnum = paragraph_num_re.match(para_text)
        if match_parnum:
            paragraph_number = match_parnum.group(1)  # e.g. '37'
            text_body = match_parnum.group(2)
        else:
            text_body = para_text

        # Find all citations in the paragraph text
        for match_obj in citation_pattern.finditer(text_body):
            full_citation = match_obj.group(0)
            d = match_obj.groupdict()

            case_name = d.get("case_name") or ""
            parenthetical = d.get("parenthetical") or None
            footnote = d.get("footnote") or None
            application_numbers = d.get("application_numbers") or None
            paragraphs_str = d.get("paragraphs") or ""
            date_ = d.get("date") or None

            # If parenthetical includes "[Committee]", split that out
            committee = None
            if parenthetical and "[Committee]" in parenthetical:
                committee = "Committee"
                parenthetical = parenthetical.replace("[Committee]", "").strip() or None

            # Fix paragraphs and parse numeric range
            paragraphs_fixed = fix_paragraphs(paragraphs_str)
            start_par_ref, end_par_ref = parse_paragraph_range(paragraphs_str)

            # start_idx = match_obj.start()
            # end_idx = match_obj.end()

            citation_info = {
                "full_citation": full_citation,
                "case_name": case_name.strip(),
                "parenthetical": parenthetical,
                "committee": committee,
                "footnote": footnote,
                "application_numbers": (
                    application_numbers.strip() if application_numbers else None
                ),
                "paragraphs_in_cited_case": paragraphs_fixed,
                "start_paragraph_in_cited_case": start_par_ref,
                "end_paragraph_in_cited_case": end_par_ref,
                "date": date_,
                "citing_paragraph": para_text,
                #'start_paragraph': start_idx,
                #'end': end_idx
            }

            all_citations.append(
                {"paragraph": paragraph_number, "citation": citation_info}
            )

    return all_citations


id_to_name = load_json(
    "/Users/ahmed/Desktop/msc-24/TND/workflow_v2.0/citation_analyzer/id_to_name.json"
)
name_to_id = load_json(
    "/Users/ahmed/Desktop/msc-24/TND/workflow_v2.0/citation_analyzer/name_to_id.json"
)
cases_names = list(id_to_name.values())


def get_citations_ids(law_section, case_id):
    results = extract_echr_citations(law_section)
    ids_map = {case_id: []}
    citation_contexts = []
    for item in results:
        # print(item)
        cited_case_name = item["citation"]["case_name"]
        cited_case_name = normalize(cited_case_name)
        match_name = find_closest_match(cited_case_name, cases_names)
        cited_case_id = None
        try:
            cited_case_id = name_to_id[match_name]
        except:
            cited_case_id = None
        if cited_case_id:
            ids_map[case_id].append(cited_case_id)
            citation_contexts.append(item["citation"])
    return ids_map, citation_contexts


def extract(case_id):
    data_path = "/Users/ahmed/Desktop/msc-24/ECHR_v2/echr_processed"
    data = load_json(os.path.join(data_path, case_id))
    law_section = data["law"]
    case_id = data["itemid"]
    ids_map, citation_contexts = get_citations_ids(law_section, case_id)
    return ids_map, citation_contexts


def analyze_zero_shot(
    current_case_path, cited_case_path, citation_context, cited_case_paragraphs_path
):
    # current case
    # current_case = load_json(os.path.join(data_path, file_name))
    current_case = load_json(current_case_path)
    current_case_name = current_case["docname"]
    current_facts = current_case["facts"]
    current_law = current_case["law"]

    # cited case
    cited_case = load_json(cited_case_path)
    cited_case_name = cited_case["docname"]
    cited_case_facts = None

    if "facts" in cited_case:
        cited_case_facts = cited_case["facts"]
    else:
        if "other" in cited_case:
            cited_case_facts = (
                "The case text do not have facts, but here is the other informative parts: "
                + cited_case["other"]
            )
        elif "procedure" in cited_case:
            cited_case_facts = (
                "The case text do not have facts, but here is the procedure part: "
                + cited_case["procedure"]
            )
        else:
            cited_case_facts = "The case text was not found."

    cited_case_law = None
    if "law" in cited_case:
        cited_case_law = cited_case["law"]
    else:
        if "relevant_law" in cited_case:
            cited_case_law = (
                "The case text do not have law, but here is the relevant law: "
                + cited_case["relevant_law"]
            )
        elif "conclusion" in cited_case:
            cited_case_law = (
                "The case text do not have law, but here is the conclusion part: "
                + cited_case["conclusion"]
            )
        else:
            cited_case_law = "The case text was not found."

    cited_case_importance = int(cited_case["importance"])
    cited_case_judgment_date = cited_case["judgementdate"]

    is_key_case = "YES" if cited_case_importance == 1 else "NO"
    importance_level = (
        "HIGH"
        if cited_case_importance in [1, 2]
        else "MEDIUM" if cited_case_importance == 3 else "LOW"
    )

    # cut the cited case facts and law if they exceed 4096 tokens
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    max_tokens = 120_000
    max_tokens -= len(encoding.encode(current_facts))
    max_tokens -= len(encoding.encode(current_law))
    max_tokens -= len(encoding.encode(cited_case_facts))
    # print('TOKENS LEFT FOR CITED CASE LAW:',max_tokens)

    cited_law_tokens = len(encoding.encode(cited_case_law))
    if cited_law_tokens > max_tokens:
        print("TRIM CITED CASE LAW: ", cited_law_tokens, " > ", max_tokens)
        cited_case_law = cited_case_law[:max_tokens]

    # citation context
    start_paragraph_in_cited_case = citation_context["start_paragraph_in_cited_case"]
    end_paragraph_in_cited_case = citation_context["end_paragraph_in_cited_case"]
    extracted_paragraphs = []
    if start_paragraph_in_cited_case and end_paragraph_in_cited_case:
        for key in cited_case:
            if key in [
                "itemid",
                "importance",
                "__articles",
                "__conclusion",
                "_decision_body",
                "article",
                "docname",
                "appno",
                "extractedappno",
                "importance",
                "itemid",
                "judgementdate",
                "parties",
                "separateopinion",
                "country",
                "rank",
                "cite",
            ]:
                continue
            else:
                needed_paras = extract_paragraphs_from_list(
                    cited_case[key].split("\n"),
                    start_paragraph_in_cited_case,
                    end_paragraph_in_cited_case,
                )
                if len(needed_paras) > 0:
                    extracted_paragraphs.append(needed_paras)
    else:
        extracted_paragraphs = (
            "The entire case text was cited with no specific paragraph mentioned"
        )

    citation_context.update({"specific_paragraphs_referenced": extracted_paragraphs})

    prompt = f"""
You are a legal expert analyzing a case and its citations.
Your task is find why the current case cited the cited case and analyze the relationship between the two cases.

Current Case:
Case Name: {current_case_name}
Facts: {current_facts}
Law: {current_law}

Citation Context:
{citation_context}

Cited Case:
Case Name: {cited_case_name}
Judgement Date: {cited_case_judgment_date}
Facts: {cited_case_facts}
Law: {cited_case_law}

When analyzing, consider:
1. Citation Location Context (if available):
   - Why is this case cited in this specific paragraph?
   - How does the citation support or relate to the argument being made in that paragraph?
   - If specific paragraphs are referenced from the cited case, what principles or reasoning from those paragraphs are being used?

2. Citation Purpose:
   - Is it supportive/distinguishing/overruling/background/procedural?
   - How does the location of the citation in the judgment inform its purpose?
   - How central is this citation to the main legal reasoning vs peripheral discussion?

3. Legal Principles:
   - What specific principles from the cited paragraphs are being referenced?
   - How do these principles connect to the argument in the citing paragraph?
   - If specific paragraphs are referenced, what key legal tests or standards do they contain?

5. Similarities and Differences:
   - Focus on aspects relevant to the specific context where citation appears
   - How do differences affect the way the citation is used in this paragraph?

Provide your analysis in JSON format with these fields:
Expected format:
{{
    "cited_case_name": "name",
    "citation_type": "supportive/distinguishing/overruling/background/procedural",
    "legal_principles": ["principles"],
    "key_similarities": ["similarities"],
    "key_differences": ["differences"],
    "reasoning": "explanation",
    "citation_context_analysis": {{
        "citing_paragraph_context": "explanation of how citation is used in this paragraph",
        "cited_paragraphs_relevance": "explanation of why these specific paragraphs were cited (if available)",
        "connection_to_argument": "how citation supports the court's reasoning at this point"
    }}
}}
"""
    response_1 = llm_call(prompt)
    response_1 = response_1.replace("```json", "").replace("```", "")
    response_1 = response_1.strip()
    try:
        response_json = json.loads(response_1)
        response_json.update({"is_key_case": is_key_case})
        response_json.update({"importance_level": importance_level})
    except:
        response_1 += (
            "is_key_case: "
            + is_key_case
            + "\n"
            + "importance_level: "
            + importance_level
        )
        response_json = response_1
        print("Error in parsing JSON, will return the response as a string")
    return response_json


def analyze_citations(case_path):

    case_name = case_path.split(".")[0]
    citation_dict, citation_contexts = extract(case_path)

    responses = []
    for value, context in zip(citation_dict[case_name], citation_contexts):
        print(value)
        data_path = "/Users/ahmed/Desktop/msc-24/ECHR/echr-processed"
        file_path = value + ".json"
        # check if the file exists
        if os.path.exists(os.path.join(data_path, file_path)):
            current_case_path = os.path.join(data_path, case_path)
            cited_case_path = os.path.join(data_path, file_path)
            cited_case_paragraphs_path = os.path.join(
                "/Users/ahmed/Desktop/msc-24/ECHR_v2/echr_processed", file_path
            )

            response = analyze_zero_shot(
                current_case_path, cited_case_path, context, cited_case_paragraphs_path
            )
            responses.append(response)
    return responses
