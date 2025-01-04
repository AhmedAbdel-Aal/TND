from openai import OpenAI
import os
import dotenv

from prompts import (
    get_summarize_facts_prompt,
    get_summarize_law_prompt,
    get_extract_legal_principles_prompt,
    get_citation_analysis_prompt,
)
from prompts import (
    get_classify_key_case_prompt,
    get_classify_three_levels_importance_prompt,
)
from prompts import get_classify_four_levels_importance_prompt
from prompts import (
    get_classify_key_case_prompt_workflow_4,
    get_classify_three_levels_importance_prompt_workflow_4,
)
from prompts import get_classify_four_levels_importance_prompt_workflow_4

from utils import load_json

dotenv.load_dotenv()


def llm_call_deepseek(prompt):

    client = OpenAI(api_key=os.getenv("DEEP_SEEK"), base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.",
            },
            {"role": "user", "content": prompt},
        ],
        stream=False,
    )

    return response.choices[0].message.content


def llm_call_openai(prompt, model="gpt-4o-mini"):

    client = OpenAI()

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an experienced legal expert specializing in European Court of Human Rights (ECHR) jurisprudence.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return completion.choices[0].message.content


def llm_call(prompt, model="gpt-4o-mini"):
    model_backend = os.getenv("MODEL")
    if model_backend == "deepseek":
        return llm_call_deepseek(prompt)
    elif model_backend == "openai":
        return llm_call_openai(prompt, model)


def check_cache(file_path, step_name):
    output_dir = "/Users/ahmed/Desktop/msc-24/TND/workflow_parallelization/results_workflow_5_facts_law"
    files = os.listdir(output_dir)
    target_file = None
    for file in files:
        if file_path in file:
            target_file = file
            break
    print(f"Target File: {target_file}")

    if not target_file:
        return None

    processed_output_file_path = os.path.join(output_dir, target_file)
    # check if a result file exists
    exists = os.path.exists(processed_output_file_path)

    # load log file
    if exists:
        log = load_json(processed_output_file_path)
        step_outputs = log["steps"][step_name]
        return step_outputs
    return None


def check_classification_cache(file_path, step_name):
    output_dir = "/Users/ahmed/Desktop/msc-24/TND/workflow_parallelization/results_workflow_5_facts_law"
    files = os.listdir(output_dir)
    target_file = None
    for file in files:
        if file_path in file:
            target_file = file
            break
    print(f"Target File: {target_file}")

    if not target_file:
        return None

    processed_output_file_path = os.path.join(output_dir, target_file)
    # check if a result file exists
    exists = os.path.exists(processed_output_file_path)

    # load log file
    if exists:
        log = load_json(processed_output_file_path)
        step_outputs = log[step_name]
        return step_outputs
    return None


def summarize_facts(facts):
    prompt = get_summarize_facts_prompt(facts)
    return llm_call(prompt)


def summarize_law(law):
    prompt = get_summarize_law_prompt(law)
    return llm_call(prompt)


def extract_legal_principles(facts, file_path=None):
    if file_path:
        cached_output = check_cache(file_path, step_name="extract_legal_principles")
        if cached_output:
            return cached_output
    prompt = get_extract_legal_principles_prompt(facts)
    return llm_call(prompt)


def perform_citation_analysis(facts, law, file_path=None):
    if file_path:
        cached_output = check_cache(file_path, step_name="citation_analysis")
        if cached_output:
            return cached_output
    prompt = get_citation_analysis_prompt(facts, law)
    return llm_call(prompt)


def classify_key_case_importance(inputs, file_path=None):
    # if file_path:
    #    cached_output = check_classification_cache(file_path, step_name = "key_case_importance")
    #    if cached_output:
    #        return cached_output
    prompt = get_classify_key_case_prompt(inputs)
    return llm_call(prompt, model="gpt-4o")


def classify_three_levels_importance(inputs, file_path=None):
    # if file_path:
    #    cached_output = check_classification_cache(file_path, step_name = "three_levels_importance")
    #    if cached_output:
    #        return cached_output
    prompt = get_classify_three_levels_importance_prompt(inputs)
    return llm_call(prompt, model="gpt-4o")


def classify_four_levels_importance(inputs):
    prompt = get_classify_four_levels_importance_prompt(inputs)
    return llm_call(prompt, model="gpt-4o")


def classify_key_case_importance_workflow_4(inputs):
    prompt = get_classify_key_case_prompt_workflow_4(inputs)
    return llm_call(prompt)


def classify_three_levels_importance_workflow_4(inputs):
    prompt = get_classify_three_levels_importance_prompt_workflow_4(inputs)
    return llm_call(prompt)


def classify_four_levels_importance_workflow_4(inputs):
    prompt = get_classify_four_levels_importance_prompt_workflow_4(inputs)
    return llm_call(prompt)
