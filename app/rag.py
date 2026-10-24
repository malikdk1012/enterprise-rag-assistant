
from pathlib import Path

import faiss
from sentence_transformers import SentenceTransformer

# Locate the project and data folders.
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
MIN_SCORE = 0.30

# Load a small model that creates text embeddings.
model = SentenceTransformer("all-MiniLM-L6-v2")


def load_documents():
    """Read all text files from the data folder."""
    documents = []

    for file_path in DATA_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")
        documents.append({
            "source": file_path.name,
            "text": text
        })

    return documents


def split_into_chunks(text, chunk_size=100, overlap=20):
    """Split text into overlapping groups of words."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must be at least zero and smaller than chunk_size"
        )

    words = text.split()
    chunks = []
    step = chunk_size - overlap

    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)

    return chunks

def search_documents(question):
    """Find relevant text using semantic similarity."""
    if not question or not question.strip():
        return []
    documents = load_documents()
    chunks = []

    for document in documents:
        for chunk in split_into_chunks(document["text"]):
            chunks.append({
                "source": document["source"],
                "text": chunk
            })

    if not chunks:
        return []

    # Convert document chunks into numerical embeddings.
    texts = [chunk["text"] for chunk in chunks]
    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    # Build a FAISS index for similarity search.
    embeddings = embeddings.astype("float32")
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)

    # Convert the user's question into an embedding.
    question_embedding = model.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")

    # Retrieve the three most similar chunks.
    top_k = min(3, len(chunks))
    scores, indices = index.search(question_embedding, top_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        if idx >= 0 and float(score) >= MIN_SCORE:
            results.append({
                "source": chunks[idx]["source"],
                "text": chunks[idx]["text"],
                "score": round(float(score), 4)
            })

    return results

