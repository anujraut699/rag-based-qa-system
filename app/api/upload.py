import os
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from app.services.ingestion import ingest_document

router = APIRouter()

UPLOAD_DIR = "data/uploads"
ALLOWED_EXTENSIONS = [".pdf", ".txt"]


@router.post("/upload")
def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    filename = file.filename.lower()

    # Check file extension
    if not any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are allowed"
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save file
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Trigger background ingestion
    background_tasks.add_task(ingest_document, file_path)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename
    }
