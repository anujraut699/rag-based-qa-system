from sentence_transformers import SentenceTransformer

# Load model once (global)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(texts: list) -> list:
    """
    Generates embeddings for a list of text chunks.
    Returns a list of vectors.
    """

    if not texts:
        return []

    embeddings = embedding_model.encode(texts)
    return embeddings
