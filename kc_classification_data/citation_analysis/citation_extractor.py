import re

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

            start_idx = match_obj.start()
            end_idx = match_obj.end()

            citation_info = {
                "full_citation": full_citation,
                "case_name": case_name.strip(),
                "parenthetical": parenthetical,
                "committee": committee,
                "footnote": footnote,
                "application_numbers": (
                    application_numbers.strip() if application_numbers else None
                ),
                "paragraphs": paragraphs_fixed,
                "start_paragraph_ref": start_par_ref,
                "end_paragraph_ref": end_par_ref,
                "date": date_,
                "start": start_idx,
                "end": end_idx,
                "citing_paragraph": para_text,
            }

            all_citations.append(
                {"paragraph": paragraph_number, "citation": citation_info}
            )

    return all_citations
