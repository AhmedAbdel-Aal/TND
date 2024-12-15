def parse_generated_response(generated_response):
    rounds = generated_response.split("---------------------")
    rounds = [round.strip() for round in rounds if round.strip()]
    parsed_rounds = []

    # For each round, separate into "Question" and "Answer" parts
    for round_text in rounds:
        if (
            "Senior Agent -> Question:" in round_text
            and "Junior Agent -> Answer:" in round_text
        ):
            # Split the round into question and answer parts
            question_part, answer_part = round_text.split("Junior Agent -> Answer:")

            # Clean up the parts by stripping leading/trailing spaces
            question_part = question_part.strip().replace("----\n", "")
            answer_part = answer_part.strip().replace("----\n", "")

            # Add the tuple (question, answer) to the list
            parsed_rounds.append(
                {
                    "question": question_part.replace(
                        "Senior Agent -> Question:", ""
                    ).strip(),
                    "answer": answer_part,
                }
            )
    return parsed_rounds
