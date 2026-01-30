def chunk_text(text: str, chunk_size: int = 500) -> list:
    """
    Splits text into fixed-size chunks.
    Returns a list of text chunks.
    """

    if not text or not text.strip():
        return []

    chunks = []

    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size].strip()
        if chunk:
            chunks.append(chunk)

    return chunks
