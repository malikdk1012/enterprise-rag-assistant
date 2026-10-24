# Enterprise RAG Assistant

An AI-powered Retrieval-Augmented Generation (RAG) application that retrieves relevant information from company documents and generates context-aware answers using a locally hosted Large Language Model (LLM).

Built to demonstrate practical skills in AI application development, backend APIs, semantic search, containerization, automated testing, and CI/CD.

## Features

- **RAG pipeline:** Combines document retrieval with LLM-generated answers.
- **Semantic search:** Generates text embeddings using Sentence Transformers.
- **Vector search:** Uses FAISS to retrieve relevant document chunks.
- **Local LLM integration:** Uses Ollama with the `qwen2.5:0.5b` model.
- **REST API:** Provides endpoints using FastAPI.
- **Source attribution:** Returns retrieved document excerpts with answers.
- **Docker and Docker Compose:** Packages and runs the application in containers.
- **Automated testing:** Uses pytest to test application functionality.
- **CI/CD:** GitHub Actions runs tests and builds the Docker image.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| FastAPI | REST API |
| Sentence Transformers | Text embeddings |
| FAISS | Vector similarity search |
| Ollama | Local LLM inference |
| Qwen 2.5 (0.5B) | Answer generation |
| Docker | Containerization |
| Docker Compose | Application orchestration |
| pytest | Automated testing |
| GitHub Actions | Continuous integration |

## How It Works

1. Load text documents from the `data/` directory.
2. Split document text into chunks.
3. Convert chunks into vector embeddings.
4. Use FAISS to retrieve relevant content for a question.
5. Send the retrieved context and question to Ollama.
6. Return the generated answer and source information through the API.

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
├── tests/
│   └── test_api.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── constraints.txt
├── .dockerignore
└── .gitignore
```

## Getting Started

### Prerequisites

- Git
- Docker Desktop with Docker Compose
- Ollama installed on the host machine
- The `qwen2.5:0.5b` model downloaded in Ollama

### Run with Docker Compose

Clone the repository:

```bash
git clone https://github.com/malikdk1012/enterprise-rag-assistant.git
cd enterprise-rag-assistant
```

Download the model and ensure Ollama is running on your host:

```bash
ollama pull qwen2.5:0.5b
```

Start the application:

```bash
docker compose up -d --build
```

Check the container:

```bash
docker compose ps
```

Open the interactive API documentation:

http://localhost:8000/docs

Check the health endpoint:

http://localhost:8000/health

Expected response:

```json
{"status": "ok"}
```

**Note:** The Compose configuration connects the container to Ollama through `host.docker.internal`. Ollama must be running and accessible on the host.

Stop the application:

```bash
docker compose down
```

### Run Locally

Create and activate a virtual environment on Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Ensure Ollama is running and the model is available:

```bash
ollama pull qwen2.5:0.5b
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Application welcome message |
| GET | `/health` | Health status |
| GET | `/search?question=...` | Retrieves relevant context and generates an answer |

### Example Search Request

```bash
curl -G "http://localhost:8000/search" --data-urlencode "question=What programming language does the team use?"
```

The response contains the question, generated answer, and retrieved sources. With the sample company documents, the answer should identify Python as a language used by the team.

## Testing

Run the automated tests:

```bash
python -m pytest -v
```

## Continuous Integration

GitHub Actions runs on pushes to `main` and pull requests targeting `main`. The workflow installs dependencies, runs automated tests, and verifies that the Docker image builds.

## Future Improvements

- Support PDF and additional document formats.
- Improve retrieval evaluation and relevance filtering.
- Add API authentication and structured logging.
- Persist vector indexes for larger document collections.
- Deploy the application to a cloud platform.
- Add performance monitoring and more integration tests.

## Author

**Deepak Kumar Malik**

Computer Science graduate interested in AI applications, backend development, and data engineering.

GitHub: https://github.com/malikdk1012/enterprise-rag-assistant
