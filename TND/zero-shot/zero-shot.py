import ollama


response = ollama.chat(
    model="mistral:7b",
    messages=[
        {"role": "system", "content": f"<s>[INST] {prompt} [/INST]"},
    ],
)
print(response["message"]["content"])
