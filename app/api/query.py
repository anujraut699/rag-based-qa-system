from fastapi import APIRouter, HTTPException, Request
from app.models.schemas import QuestionRequest, AnswerResponse
from app.core.embeddings import generate_embeddings
from app.core.vector_store import search_faiss
from app.core.llm import generate_answer
from app.utils.rate_limiter import rate_limit

router = APIRouter()


@router.post("/ask", response_model=AnswerResponse)
def ask_question(request: Request, payload: QuestionRequest):
    # Apply rate limiting
    rate_limit(request)

    question = payload.question.strip()

    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    question_embedding = generate_embeddings([question])

    retrieved_chunks = search_faiss(question_embedding)

    if not retrieved_chunks:
        raise HTTPException(
            status_code=404,
            detail="No documents available or no relevant context found"
        )

    answer = generate_answer(question, retrieved_chunks)

    return {
        "answer": answer,
        "context_used": retrieved_chunks
    }
