from transformers import pipeline

# Load model once
qa_pipeline = pipeline(
    "text-generation",
    model="distilgpt2",
    max_new_tokens=150
)


def generate_answer(question: str, context_chunks: list) -> str:
    """
    Generates answer using retrieved context.
    """

    if not context_chunks:
        return "No relevant information found in documents."

    context_text = "\n".join(context_chunks)

    prompt = (
        "Answer the question using only the context below.\n\n"
        f"Context:\n{context_text}\n\n"
        f"Question:\n{question}\n\n"
        "Answer:"
    )

    response = qa_pipeline(prompt)[0]["generated_text"]

    return response.split("Answer:")[-1].strip()
