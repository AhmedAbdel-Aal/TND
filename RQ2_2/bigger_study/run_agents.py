import os
import time
import ollama
import json
from utils import load_json, save_json
from agent_senior import SeniorAgent
from agent_junior import JuniorAgent
from utils import (
    get_last_question,
    check_for_stop,
    check_for_final_answer,
    save_txt_file,
)


# specify the backend and the model
backend = "openai"  #'groq'
model = "gpt-4o"  #'llama3-70b-8192'#'gemma2-9b-it'#'mixtral-8x7b-32768'
input_dir = "../bigger_study_sample/"
output_dir = "./" + backend + "_" + model + "/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
else:
    print("else")

# get case number as input from user
# case_number = input("Enter case number: ")
# c4 = load_json('../bigger_study_sample/'+ case_number +'.json')

# get list of all cases
files = os.listdir("../bigger_study_sample/")


def run_conversation(s_agent, j_agent, case):
    round = 20
    all_conversation = ""

    for i in range(round):
        print(f"---------------------round{i+1}-------------------------")
        all_conversation += (
            f"---------------------round{i+1}-------------------------\n"
        )
        response = s_agent.ask_question()
        question = get_last_question(response)
        # print(f"Q: {question}")
        stop = check_for_stop(response)
        final_answer = check_for_final_answer(response)
        if (stop is not None) or (final_answer is not None):
            # print(f"Stop: {stop}, final_answer: {final_answer}")
            print(response)
            all_conversation += f"\n{response}"
            break

        input_string = None
        if "procedure" in case:
            input_string = case["procedure"] + "\n" + case["facts"]
        else:
            input_string = case["facts"]

        answer = j_agent.answer_question(input_string, case["conclusion"], question)
        s_agent.append_to_cache(answer)

        print(f"Senior Agent -> {question}")
        print(f"Junior Agent -> {answer}")

        all_conversation += (
            f"Senior Agent -> {question}\n\nJunior Agent -> {answer}\n\n"
        )
        time.sleep(20)
    return all_conversation


if __name__ == "__main__":
    print(f"I will work on {len(files)} cases")
    for case_number in files:
        if case_number != "001-155352.json":
            continue
        s_agent = SeniorAgent(model_name=model, backend=backend)
        j_agent = JuniorAgent(model_name=model, backend=backend)
        print("case_number: ", case_number)
        case_data = load_json(input_dir + case_number)
        print("loaded case: ", case_number)
        all_conversation = run_conversation(s_agent, j_agent, case_data)
        save_txt_file(
            output_dir + case_data["itemid"] + "_output.txt", all_conversation
        )
        time.sleep(60)
