# Enterprise RAG Assistant

An AI-powered Retrieval-Augmented Generation (RAG) application that answers questions using company documents. Built with Python, FastAPI, Sentence Transformers, FAISS, Docker, and GitHub Actions.

## Project Overview

This project demonstrates how an enterprise-style assistant retrieves relevant information from internal documents and uses a local language model to generate context-based answers.

## Features

- **Document retrieval:** Loads text documents from the data directory.
- **Semantic search:** Uses Sentence Transformers to generate text embeddings.
- **Vector search:** Uses FAISS to retrieve relevant document chunks.
- **REST API:** Exposes endpoints through FastAPI.
- **AI-generated answers:** Integrates with Ollama and a local language model.
- **Docker:** Packages the application into a container.
- **Automated testing:** Uses pytest to test core functionality.
- **CI/CD:** GitHub Actions runs tests and verifies the Docker image builds.

## Technology Stack

- Python
- FastAPI
- Sentence Transformers (`all-MiniLM-L6-v2`)
- FAISS
- Ollama (`qwen2.5:0.5b`)
- Docker
- pytest
- GitHub Actions

## Project Structure

```text
enterprise-rag-assistant/
├── app/
│   ├── main.py
│   ├── rag.py
│   └── test_rag.py
├── data/
│   ├── company_info.txt
│   └── company.txt
├── .github/workflows/ci.yml
├── Dockerfile
├── .dockerignore
├── .gitignore
├── requirements.txt
└── constraints.txt
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Checks whether the application is running |
| GET | `/health` | Returns the application health status |
| GET | `/search?question=...` | Retrieves relevant context and generates an answer |

Interactive API documentation is available at `/docs` while the application is running.

## Run Locally

### 1. Install dependencies

Use Python 3.12 or another compatible Python version.

```bash
pip install -r requirements.txt
```

### 2. Start Ollama

Install Ollama and download the configured model:

```bash
ollama pull qwen2.5:0.5b
```

Make sure Ollama is running.

### 3. Start the API

```bash
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` in your browser.

### 4. Run tests

```bash
python -m pytest -v
```

### 5. Build the Docker image

```bash
docker build -t enterprise-rag-assistant .
```

When running in Docker, configure `OLLAMA_URL` to point to an Ollama service accessible from the container.

## Automated Workflow

GitHub Actions runs when code is pushed to `main` or a pull request targets `main`. The workflow installs dependencies, runs the tests, and builds the Docker image.

## Future Improvements

- Support PDF and additional document formats.
- Evaluate retrieval quality and improve relevance filtering.
- Add API authentication and structured logging.
- Deploy the application to a cloud platform.
- Expand automated tests and monitoring.

## Author

**Deepak Kumar Malik**

Computer Science portfolio project focused on AI, backend development, and data engineering fundamentals.
