from PyPDF2 import PdfReader


def load_text_from_file(file_path: str) -> str:
    """
    Reads text from PDF or TXT files.
    Returns empty string if no text found.
    """

    if file_path.lower().endswith(".txt"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""

    if file_path.lower().endswith(".pdf"):
        try:
            reader = PdfReader(file_path)
            text = ""

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            return text.strip()
        except Exception:
            return ""

    return ""
