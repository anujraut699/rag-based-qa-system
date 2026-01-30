from app.utils.file_loader import load_text_from_file
from app.core.chunking import chunk_text
from app.core.embeddings import generate_embeddings
from app.core.vector_store import add_embeddings_to_faiss


def ingest_document(file_path: str):
    """
    Background ingestion job:
    - Read document
    - Chunk text
    - Generate embeddings
    - Store in FAISS
    """

    print(f"Starting ingestion for: {file_path}")

    text = load_text_from_file(file_path)

    if not text.strip():
        print(f"No readable text found in {file_path}. Skipping.")
        return

    chunks = chunk_text(text)

    if len(chunks) == 0:
        print(f"No chunks created for {file_path}. Skipping.")
        return

    embeddings = generate_embeddings(chunks)

    if len(embeddings) == 0:
        print("Embedding generation failed. Skipping.")
        return

    add_embeddings_to_faiss(embeddings, chunks)

    print(f"Stored {len(chunks)} chunks in FAISS")
