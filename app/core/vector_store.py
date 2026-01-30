import os
import faiss
import pickle

INDEX_PATH = "data/faiss_index/index.faiss"
TEXT_PATH = "data/faiss_index/chunks.pkl"


def save_faiss_index(index, chunks):
    faiss.write_index(index, INDEX_PATH)
    with open(TEXT_PATH, "wb") as f:
        pickle.dump(chunks, f)


def load_faiss_index():
    if not os.path.exists(INDEX_PATH) or not os.path.exists(TEXT_PATH):
        return None, []

    index = faiss.read_index(INDEX_PATH)
    with open(TEXT_PATH, "rb") as f:
        chunks = pickle.load(f)

    return index, chunks


def add_embeddings_to_faiss(embeddings, chunks):
    """
    Adds embeddings and chunks to FAISS.
    Creates new index if not exists.
    """

    dimension = len(embeddings[0])

    index, existing_chunks = load_faiss_index()

    if index is None:
        index = faiss.IndexFlatL2(dimension)
        existing_chunks = []

    index.add(embeddings)
    existing_chunks.extend(chunks)

    save_faiss_index(index, existing_chunks)


def search_faiss(query_embedding, top_k=3):
    """
    Searches FAISS index and returns top matching chunks.
    """

    index, chunks = load_faiss_index()

    if index is None or index.ntotal == 0:
        return []

    distances, indices = index.search(query_embedding, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(chunks):
            results.append(chunks[idx])

    return results
