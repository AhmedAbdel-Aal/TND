import dotenv
import os
import time
from tqdm import tqdm
import pandas as pd
from utils import (
    load_json,
    save_json,
    text_to_json,
    construct_other_agents_answer,
    format_prompt,
)
import logging
import argparse
from prompts import system_prompt, prompt
from agent import Agent

dotenv.load_dotenv()

# diabsle deprecation warning
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

## configs
input_data_root = "/Users/ahmed/Desktop/msc-24/ECHR/echr-processed"
input_files_path = (
    "/Users/ahmed/Desktop/msc-24/TND/kc_classification_data/pre_cutoff_data_new"
)
output_dir = "./results_openai/"
backend = "openai"


def read_data():

    df_1 = pd.read_csv(os.path.join(input_files_path, "df_1.csv"))
    list_1 = df_1["file_path"].to_list()

    df_2 = pd.read_csv(os.path.join(input_files_path, "df_2.csv"))
    list_2 = df_2["file_path"].to_list()

    df_3 = pd.read_csv(os.path.join(input_files_path, "df_3.csv"))
    list_3 = df_3["file_path"].to_list()

    df_4 = pd.read_csv(os.path.join(input_files_path, "df_4.csv"))
    list_4 = df_4["file_path"].to_list()

    return list_1, list_2, list_3, list_4


def check_processed_files(paths_list, output_dir):
    already_processed_files = os.listdir(output_dir)

    # remove the prefix kc_ and not_kc_
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

    left_files = list(set(paths_list) - set(already_processed_files))
    return left_files


def infere(paths_list, output_dir, backend, n_agents, rounds):

    left_files = check_processed_files(paths_list, output_dir)

    for file_path in tqdm(left_files):
        try:
            case_path = os.path.join(input_data_root, file_path)
            case_data = load_json(case_path)
            case_facts = case_data["facts"]
            data = {"facts": case_facts}
            output_result = {}

            agents = []
            for i in range(n_agents):
                print(f"Creating agent {i}")
                agent = Agent(name=f"Agent_{i+1}", backend=backend)
                agent.add_to_context("system", system_prompt)
                agents.append(agent)

            rounds_stats = {}
            # classify the case
            for round in range(1, rounds + 1):
                print(f"Round {round}")
                # call the agents
                for agent in agents:
                    if round == 1:
                        prompt_formatted = format_prompt(prompt, **data)
                        agent.add_to_context("user", prompt_formatted)
                        response = agent.call()
                        agent.add_to_context("assistant", response)
                    else:
                        other_responses = construct_other_agents_answer(agents, agent)
                        agent.add_to_context("user", other_responses)
                        response = agent.call()
                        agent.add_to_context("assistant", response)

                # collect the responses
                not_key_case_agents = []
                key_case_agents = []
                majority_vote = None

                for agent in agents:

                    response = agent.get_latest_response()
                    parsed_response = text_to_json(response)
                    if "not key case" in parsed_response["classification"].lower():
                        # print(f'{agent.name} classified as NO KEY CASE')
                        not_key_case_agents.append(agent.name)
                    elif "key case" in parsed_response["classification"].lower():
                        # print(f'{agent.name} classified as KEY CASE')
                        key_case_agents.append(agent.name)
                    else:
                        print("Invalid response")

                if len(key_case_agents) > len(not_key_case_agents):
                    majority_vote = "key case"
                    print(
                        "The case is a KEY CASE by majority vote --> {} agents < {} agents".format(
                            not_key_case_agents, key_case_agents
                        )
                    )
                elif len(key_case_agents) < len(not_key_case_agents):
                    majority_vote = "not key case"
                    print(
                        "The case is NOT a KEY CASE by majority vote -> {} agents > {} agents".format(
                            not_key_case_agents, key_case_agents
                        )
                    )
                else:
                    majority_vote = "undecided - equal votes"
                    print("The case is UNDECIDED by majority vote")

                rounds_stats[f"round_{round}"] = {
                    "key_case": key_case_agents,
                    "not_key_case": not_key_case_agents,
                    "majority_vote": majority_vote,
                }
                output_result[f"round_{round}"] = rounds_stats[f"round_{round}"]

                if len(key_case_agents) == 0 or len(not_key_case_agents) == 0:
                    print(
                        "Agents reached consensus"
                    )  # will not break, we need to collect reaosnings to see if it will be any better
                    rounds_stats[f"round_{round}"]["consensus"] = True
                else:
                    rounds_stats[f"round_{round}"]["consensus"] = False

            # write the result to a file

            for agent in agents:
                output_result[agent.name] = agent.get_trace()

            output_result["importance"] = case_data["importance"]

            path = os.path.join(
                output_dir, f'i_{case_data["importance"]}_case_{file_path}'
            )
            save_json(path, output_result)
            time.sleep(3)

        except Exception as e:
            logging.error(f"Error in case: {file_path}")
            logging.error(e)


def main(output_dir, backend, agents, rounds):
    list_1, list_2, list_3, list_4 = read_data()
    print(f"Number of cases in list 1: {len(list_1)}")
    infere(list_1, output_dir, backend, agents, rounds)
    print(f"Number of cases in list 2: {len(list_2)}")
    infere(list_2, output_dir, backend, agents, rounds)
    print(f"Number of cases in list 3: {len(list_3)}")
    infere(list_3, output_dir, backend, agents, rounds)
    print(f"Number of cases in list 4: {len(list_4)}")
    infere(list_4, output_dir, backend, agents, rounds)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the script with a specified backend."
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        required=True,
        help="Specify the output directory as a string.",
    )

    # Add the 'backend' argument
    parser.add_argument(
        "--backend", type=str, required=True, help="Specify the backend as a string."
    )

    parser.add_argument(
        "--n_agents", type=int, default=2, help="Specify the number of agents."
    )

    parser.add_argument(
        "--rounds", type=int, default=3, help="Specify the number of roundsd."
    )

    # Parse the arguments
    args = parser.parse_args()

    # Access the backend argument
    backend = args.backend
    output_dir = args.output_dir
    n_agents = args.n_agents
    rounds = args.rounds

    # checl for output directory
    output_dir = output_dir + "_" + backend + "_a" + str(n_agents) + "_r" + str(rounds)
    print(f"Output directory: {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    main(output_dir, backend, n_agents, rounds)


## python inference.py --output_dir results_openai --backend openai --n_agents 2 --rounds 2
