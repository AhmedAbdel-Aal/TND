from retriever import GTR


def generate_response(question: str, llm: LLM, retriever: Retriever, k: int = 10):
    docs = retriever.retrieve(question, k=k)

    docs = [doc[0] for doc in docs]

    paragraphs = "\n".join(
        [
            f"[Doc {i+1}]: "
            + GTR.remove_par_text_prefix(
                doc.page_content,
                doc.metadata["case_name"],
                doc.metadata["paragraph_number"],
            )
            for i, doc in enumerate(docs)
        ]
    )

    prompt = f"""
    You are an ECHR legal expert tasked to answer a question.
    The following documents were retrieved and should help you answer the question:
    {paragraphs}

    Instructions:
    Use the retrieved documents to answer the question.
    Reuse the language from the documents!
    Cite relevant documents at the end of a sentence!
    Accepted formats: sentence [citation(s)].
    Valid citation formats: [Doc 1] or [Doc 1, Doc 2, Doc 3]
    You must follow the [Doc i] format! Do NOT use the case names or paragraph numbers to cite documents!
    You should NOT provide a list of all used citations at the end of your response!

    Question: {question}
    Answer:
    """

    response = llm.infer_completion(prompt)
    return response, docs
