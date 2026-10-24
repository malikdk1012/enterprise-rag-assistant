
from unittest.mock import Mock

import requests
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Enterprise RAG Assistant is running!"
    }


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_search_rejects_empty_question():
    response = client.get("/search", params={"question": ""})

    assert response.status_code == 422


def test_search_returns_answer(monkeypatch):
    documents = [
        {
            "source": "company.txt",
            "score": 0.9,
            "text": "The engineering team uses FastAPI.",
        }
    ]

    monkeypatch.setattr(
        "app.main.search_documents",
        lambda question: documents,
    )

    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "response": "The team uses FastAPI."
    }

    monkeypatch.setattr(
        "app.main.requests.post",
        lambda *args, **kwargs: mock_response,
    )

    response = client.get(
        "/search",
        params={"question": "Which framework is used?"},
    )

    assert response.status_code == 200
    assert response.json()["answer"] == "The team uses FastAPI."
    assert response.json()["sources"] == documents


def test_search_returns_no_information_when_no_documents_found(
    monkeypatch,
):
    monkeypatch.setattr(
        "app.main.search_documents",
        lambda question: [],
    )

    response = client.get(
        "/search",
        params={"question": "Unknown information"},
    )

    assert response.status_code == 200
    assert response.json()["sources"] == []
    assert "No relevant information" in response.json()["answer"]


def test_search_handles_document_search_error(monkeypatch):
    def failing_search(question):
        raise RuntimeError("Search failed")

    monkeypatch.setattr(
        "app.main.search_documents",
        failing_search,
    )

    response = client.get(
        "/search",
        params={"question": "Test question"},
    )

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "Document search failed. Please try again."
    )


def test_search_handles_ai_timeout(monkeypatch):
    monkeypatch.setattr(
        "app.main.search_documents",
        lambda question: [
            {"source": "company.txt", "score": 0.9, "text": "Example"}
        ],
    )

    def timeout_request(*args, **kwargs):
        raise requests.Timeout("Request timed out")

    monkeypatch.setattr(
        "app.main.requests.post",
        timeout_request,
    )

    response = client.get(
        "/search",
        params={"question": "Test question"},
    )

    assert response.status_code == 504


def test_search_handles_ai_service_unavailable(monkeypatch):
    monkeypatch.setattr(
        "app.main.search_documents",
        lambda question: [
            {"source": "company.txt", "score": 0.9, "text": "Example"}
        ],
    )

    def failed_request(*args, **kwargs):
        raise requests.ConnectionError("Service unavailable")

    monkeypatch.setattr(
        "app.main.requests.post",
        failed_request,
    )

    response = client.get(
        "/search",
        params={"question": "Test question"},
    )

    assert response.status_code == 503
