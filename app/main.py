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

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate",
)
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:0.5b")


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
        result["text"] for result in results
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

    prompt = f"""Answer the question using only the company context below.
If the answer is not available in the context, say you could not find it.

Company context:
{context}

Question: {question}

Answer:"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
        answer = response.json().get("response")

        if not answer:
            raise HTTPException(
                status_code=502,
                detail="The AI service returned an empty answer.",
            )

    except requests.Timeout:
        raise HTTPException(
            status_code=504,
            detail="The AI service took too long to respond. Please try again.",
        )
    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="The AI service is unavailable. Please try again later.",
        )
    except ValueError:
        raise HTTPException(
            status_code=502,
            detail="The AI service returned an invalid response.",
        )

    return {
        "question": question,
        "answer": answer,
        "sources": results,
    }
