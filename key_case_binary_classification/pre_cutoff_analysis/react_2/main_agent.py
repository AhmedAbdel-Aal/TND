from langchain.agents import Tool
from langchain.chat_models import ChatOpenAI
import os
import dotenv
import time
import warnings
import IPython
import sys
from tqdm import tqdm
import pandas as pd
from utils import load_json, save_json, from_input_path_to_output_path
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.callbacks.manager import CallbackManager
from LegalPrincipleExtractorTool import LegalPrincipleExtractor
from CitationExtractorTool import CitationExtractor
from legalHelperTool import LegalHelper
from FactsReaderTool import CaseFactsReader
from LawReaderTool import CaseLawReader
from AgentLogging import AgentLoggingCallback
from prompts import get_legal_react_prompt

dotenv.load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

## configs
input_data_root = "../../../../ECHR/echr-processed/"
output_dir = "./results_openai_gpt4-mini/"
backend = "openai"

# Disable all DeprecationWarnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# If needed, you can also suppress warnings at the Python interpreter level
os.environ["PYTHONWARNINGS"] = "ignore::DeprecationWarning"


llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini", openai_api_key=openai_api_key)


tools = [
    Tool(
        name="facts_reader",
        func=CaseFactsReader()._run,
        description="""
            Load and return the case facts.
            Requires 'case_path' as input.
            """,
    ),
    Tool(
        name="law_reader",
        func=CaseLawReader()._run,
        description="Load and return the case law.",
    ),
    Tool(
        name="legal_principle_extractor",
        func=LegalPrincipleExtractor()._run,
        description="Extract key legal principles from the case file.",
    ),
    Tool(
        name="citation_extractor",
        func=CitationExtractor()._run,
        description="Extract citations from the case file.",
    ),
    Tool(
        name="legal_helper",
        func=LegalHelper()._run,
        description="""A tool to answer specific legal questions about ECHR jurisprudence and legal principles.
    Use this tool to ask focused questions about legal concepts, doctrines, or interpretations that will help  analyze the case.
    Do NOT ask this tool to determine if a case is key - instead ask specific questions  about legal elements you identify from the principles and citations.
    To use this tool you must provide [file_path, question] as input.
    """,
    ),
]


def run_agent(case_path):

    # prompt = hub.pull("hwchase17/react")
    prompt = get_legal_react_prompt()
    agent = create_react_agent(llm, tools, prompt)
    # Create the callback handler
    logger = AgentLoggingCallback()
    callback_manager = CallbackManager([logger])

    # Create agent executor with the callback
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        callback_manager=callback_manager,
    )
    leagl_prompt = f"""Classify the importance of the legal case at {case_path}.
      Your Final Answer: CLASSIFICATION: [NOT KEY CASE or KEY CASE]"""  # get_prompt(case_path)
    result = agent_executor.invoke(
        {"input": leagl_prompt, "case_path": case_path}, {"callbacks": [logger]}
    )

    # Return both the result and the logs
    return {"result": result, "logs": logger.logs}


def read_data():
    df_1 = pd.read_csv("../../../kc_classification_data/pre_cutoff_data/df_1.csv")
    list_1 = df_1["file_path"].to_list()

    df_2 = pd.read_csv("../../../kc_classification_data/pre_cutoff_data/df_2.csv")
    list_2 = df_2["file_path"].to_list()

    df_3 = pd.read_csv("../../../kc_classification_data/pre_cutoff_data/df_3.csv")
    list_3 = df_3["file_path"].to_list()

    df_4 = pd.read_csv("../../../kc_classification_data/pre_cutoff_data/df_4.csv")
    list_4 = df_4["file_path"].to_list()

    return list_1, list_2, list_3, list_4


def check_processed_files(output_dir):
    already_processed_files = os.listdir(output_dir)

    # remove the prefixs
    already_processed_files = [
        f.replace("i_1_case_", "") for f in already_processed_files
    ]
    already_processed_files = [
        f.replace("i_2_case_", "") for f in already_processed_files
    ]
    already_processed_files = [
        f.replace("i_3_case_", "") for f in already_processed_files
    ]
    already_processed_files = [
        f.replace("i_4_case_", "") for f in already_processed_files
    ]

    error_files = []
    for file in already_processed_files:
        logged_file_path = from_input_path_to_output_path(input_data_root + file)
        logged_file = load_json(logged_file_path)
        if (
            "Agent stopped due to iteration limit or time limit"
            in logged_file["result"]["output"]
        ):
            error_files.append(file)

    print(f"Number of error files: {len(error_files)}")
    # remove the error files from already_processed_files
    already_processed_files = list(set(already_processed_files) - set(error_files))
    return already_processed_files


def infere(paths_list, prefix):
    # already_processed_files = check_processed_files(output_dir)
    # paths_list = list(set(paths_list) - set(already_processed_files))

    for file_path in tqdm(paths_list):
        # read the case file
        # if file_path in already_processed_files:
        #    continue
        try:
            case_path = os.path.join(input_data_root, file_path)
            case_data = load_json(case_path)

            # run the agent
            result = run_agent(case_path)
            result["importance"] = case_data["importance"]
            result["date"] = case_data["judgementdate"]

            # save the result
            save_json(os.path.join(output_dir, f"i_{prefix}_case_{file_path}"), result)

            # sleep to avoid rate limiting
            time.sleep(60)
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
            continue


def main():
    list_1, list_2, list_3, list_4 = read_data()
    print(f"Number of cases in list 1: {len(list_1)}")
    infere(list_1, "1")
    print(f"Number of cases in list 2: {len(list_2)}")
    # infere(list_2, "2")
    print(f"Number of cases in list 3: {len(list_3)}")
    # infere(list_3, "3")
    print(f"Number of cases in list 4: {len(list_4)}")
    # infere(list_4, "4")


if __name__ == "__main__":
    main()
