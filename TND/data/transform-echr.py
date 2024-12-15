from tqdm import tqdm
from utils import *


def clean_text(text):
    return text.replace("\xa0", " ")


def flatten_elements(elements_list):
    content_list = ""

    for element in elements_list:
        content_list += clean_text(element["content"])

        if len(element["elements"]) > 0:
            content_list += flatten_elements(element["elements"])
    return content_list


def get_content(sections):
    r = {}
    for section in sections:
        content, elements = section["content"], section["elements"]

        if "section_name" not in section.keys():
            section_name = "other"
        else:
            section_name = section["section_name"]

        elements = flatten_elements(elements)

        if section_name not in r.keys():
            r[section_name] = elements
        else:
            r[section_name] = r[section_name] + elements
    return r


def transofrm_2_0_0(st, ust, output_directory):
    keys = list()
    for i, j in tqdm(zip(st, ust)):
        case = {}
        assert i["itemid"] == j["itemid"]

        docx_key = list(j["content"].keys())[0]
        sections = j["content"][docx_key]

        case["itemid"] = i["itemid"]
        case["importance"] = i["importance"]
        case["judgementdate"] = i["judgementdate"]
        r = get_content(sections)
        keys.extend(list(r.keys()))
        case.update(r)

        save_json(case, output_directory + i["itemid"] + ".json")


if __name__ == "__main__":
    structured_path = "<PATH_TO_DATA_DIRECTORY>/echr_2_0_0_structured_cases.json"
    st = load_json(structured_path)

    unstructured_path = "<PATH_TO_DATA_DIRECTORY>/echr_2_0_0_unstructured_cases.json"
    ust = load_json(unstructured_path)

    output_directory = "<PATH_TO_PROCESSED_DATA_DIRECTORY>/echr-processed/"

    transofrm_2_0_0(st, ust, output_directory)
