import re

# List of keys we are interested in
TARGET_KEYS = [
    "Originating Body",
    "Document Type",
    "Title",
    "App. No(s)",
    "Importance Level",
    "Respondent State(s)",
    "Judgment Date",
    "Decision Date",
    "Applicability",
    "Conclusion(s)",
    "Article(s)",
    "Rules of Court",
    "Separate Opinion(s)",
    "Domestic Law",
    "Keywords",
]


def parse_case_files(case_text):
    import re

    # Regular expression to match section headers
    # section_pattern = r"(?m)^(INTRODUCTION|PROCEDURE|THE FACTS|THE LAW|RELEVANT LEGAL FRAMEWORK|RELEVANT LEGAL FRAMEWORK AND PRACTICE|CONCLUSION|FOR THESE REASONS, THE COURT)$"
    section_pattern = r"(?m)^(INTRODUCTION|PROCEDURE|THE FACTS|THE LAW|RELEVANT LEGAL FRAMEWORK(?: AND PRACTICE)?|CONCLUSION|FOR THESE REASONS, THE COURT(?:,.*)?)$"

    # Split content based on section headers
    sections = re.split(section_pattern, case_text)

    # Sections may include extraneous table of contents references; process them
    extracted_data = {}
    for i in range(1, len(sections), 2):
        header = sections[i].strip()
        text = sections[i + 1].strip()

        # Exclude table of contents if it's too short or contains only pointers
        if header not in extracted_data:
            extracted_data[header] = text
        else:
            # Append only if the current section content seems substantive
            if len(text) > len(extracted_data[header]):
                extracted_data[header] = text
    return extracted_data


def parse_metadata_files(lines):
    # Dictionary to store extracted data
    extracted_data = {}

    # Initialize variables to track the current key and value
    current_key = None
    current_value = []

    for line in lines:
        line = line.strip()
        if not line:
            continue  # Skip empty lines

        # Check if the line is a key (from the TARGET_KEYS list)
        if line in TARGET_KEYS:
            # If we were collecting a value for a previous key, save it
            if current_key:
                extracted_data[current_key] = " ".join(current_value).strip()

            # Start a new key
            current_key = line
            current_value = []  # Reset the value collector

        else:
            # Append the current line to the value collector
            current_value.append(line)

    # Add the last collected key-value pair
    if current_key:
        extracted_data[current_key] = " ".join(current_value).strip()

    return extracted_data


def parse_oneliner_files(lines):
    case_summaries = []
    collecting = False
    current_summary = []

    for line in lines:
        line = line.strip()
        # print(line, current_summary)

        # If we encounter "Key cases XXXX", save any previous summary and reset
        if re.match(r"^Key cases \d{4}$", line):
            if collecting:
                # Save the previous summary (content before "Key cases" if any)
                case_summaries.append(" ".join(current_summary))
            collecting = True
            current_summary = []  # Start a new summary without "Key cases XXXX"

        # Stop collecting when encountering "Legal summary"
        elif "Legal summary" in line:
            if collecting:
                case_summaries.append(" ".join(current_summary))
                collecting = False
                current_summary = []

        # Collect all other lines
        elif collecting or line:  # Collect even before "Key cases XXXX"
            collecting = True
            current_summary.append(line)

    # Save any remaining content at the end of the file
    if current_summary:
        case_summaries.append(" ".join(current_summary))

    # return '/n'.join(case_summaries)
    return case_summaries
