import os
from pathlib import Path

import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse

from app.rag import search_documents

app = FastAPI(
    title="Enterprise RAG Assistant",
    description="Search company documents and generate answers using RAG.",
    version="1.0.0",
)

PROJECT_DIR = Path(__file__).resolve().parent
CHAT_PAGE = PROJECT_DIR / "static" / "index.html"

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")


@app.get("/")
def home():
    return {"message": "Enterprise RAG Assistant is running!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/chat", include_in_schema=False)
def chat():
    if not CHAT_PAGE.is_file():
        raise HTTPException(
            status_code=404,
            detail="Chat webpage not found.",
        )
    return FileResponse(CHAT_PAGE)


@app.get("/search")
def search(
    question: str = Query(..., min_length=1, max_length=1000),
):
    question = question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Please enter a question.",
        )

    try:
        results = search_documents(question)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Document search failed. Please try again.",
        )

    context = "\n\n".join(
        result["text"]
        for result in results
        if result.get("text")
    )

    if not context:
        return {
            "question": question,
            "answer": (
                "No relevant information was found "
                "in the company documents."
            ),
            "sources": [],
        }

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="AI service is not configured.",
        )

    try:
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Answer using only the supplied company "
                            "context. If the answer is not available "
                            "in the context, say you could not find it."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Company context:\n{context}\n\n"
                            f"Question: {question}"
                        ),
                    },
                ],
                "temperature": 0.2,
            },
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        answer = data["choices"][0]["message"]["content"]

        if not answer:
            raise HTTPException(
                status_code=502,
                detail="The AI service returned an empty answer.",
            )

    except requests.Timeout:
        raise HTTPException(
            status_code=504,
            detail="The AI service timed out. Please try again.",
        )
    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="The AI service is unavailable. Please try again later.",
        )
    except (ValueError, KeyError, IndexError, TypeError):
        raise HTTPException(
            status_code=502,
            detail="The AI service returned an invalid response.",
        )

    return {
        "question": question,
        "answer": answer,
        "sources": results,
    }
