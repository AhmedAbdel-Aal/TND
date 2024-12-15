import os
import time
import ollama
import json
from utils import load_json, save_json, load_txt
from agent_senior import SeniorAgent
from agent_junior import JuniorAgent
from utils import (
    get_last_question,
    check_for_stop,
    check_for_final_answer,
    save_txt_file,
)


# specify the backend and the model
backend = "groq"
model = "llama3-70b-8192"  #'gemma2-9b-it'#'mixtral-8x7b-32768'
input_dir = "../bigger_study_sample/extension/"
output_dir = "./" + backend + "_" + model + "/extension/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
else:
    print("else")


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
    # get list of all cases
    cases = os.listdir("../bigger_study_sample/extension/")
    print(cases)
    for idx, case in enumerate(cases):
        if idx != 1:
            continue
        case_number = str(case)
        case_data = {
            "itemid": case_number,
            "facts": load_txt(
                "../bigger_study_sample/extension/" + case_number + "/facts.txt"
            ),
            "law": load_txt(
                "../bigger_study_sample/extension/" + case_number + "/law.txt"
            ),
            "conclusion": load_txt(
                "../bigger_study_sample/extension/" + case_number + "/conclusion.txt"
            ),
        }

        s_agent = SeniorAgent(model_name=model, backend=backend)
        j_agent = JuniorAgent(model_name=model, backend=backend)
        print("case_number: ", case_number)
        all_conversation = run_conversation(s_agent, j_agent, case_data)
        save_txt_file(
            output_dir + case_data["itemid"] + "_output.txt", all_conversation
        )
        time.sleep(60)
