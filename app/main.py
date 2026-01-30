from fastapi import FastAPI
from app.api import upload, query

app = FastAPI(title="RAG-Based Question Answering System")

app.include_router(upload.router)
app.include_router(query.router)


@app.get("/")
def health_check():
    return {"status": "API is running"}
