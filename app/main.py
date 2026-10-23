import os

from fastapi import FastAPI, Query
import requests

from app.rag import search_documents

app = FastAPI(title="Enterprise RAG Assistant")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = "qwen2.5:0.5b"


@app.get("/")
def home():
    return {"message": "Enterprise RAG Assistant is running!"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/search")
def search(question: str = Query(..., min_length=1)):
    try:
        # Step 1: Find relevant information in company documents
        results = search_documents(question)

        # Step 2: Prepare the context for the AI model
        context = "\n\n".join(
            result["text"] for result in results
        )

        if not context:
            return {
                "question": question,
                "answer": "No relevant information was found in the company documents.",
                "sources": []
            }

        prompt = f"""Answer the question using only the company context below.
If the answer is not available in the context, say you could not find it.

Company context:
{context}

Question: {question}

Answer:"""

        # Step 3: Ask the local Ollama model to answer
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()
        answer = response.json()["response"]

        # Step 4: Return the answer and its sources
        return {
            "question": question,
            "answer": answer,
            "sources": results
        }

    except Exception as error:
        return {
            "error": "The search request failed.",
            "debug_error": str(error)
        }


