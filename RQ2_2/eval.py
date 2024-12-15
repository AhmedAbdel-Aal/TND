import os
from rouge_score import rouge_scorer
import ollama
from groq import Groq


def rouge_score(hypothesis, reference):
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    scores = scorer.score(hypothesis, reference)
    return scores


def get_completion(
    backend, model, prompt, system_message="You are a helpful assistant."
):
    if backend == "ollama":
        response = ollama.chat(
            model="llama3:8b",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
        )
        return response["message"]["content"]
    elif backend == "groq":
        groq_client = Groq(api_key=os.getenv("GROQ_API_TOKEN"))
        chat_completion = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
        )
        return chat_completion.choices[0].message.content
    else:
        raise ValueError("Please provide a valid inference: 'ollama' or 'groq'")


def llm_eval(hypothesis, reference):
    return 0
