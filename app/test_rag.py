
from rag import load_documents, search_documents, split_into_chunks


def test_documents_are_loaded():
    documents = load_documents()

    assert len(documents) > 0
    assert any(
        document["source"] == "company_info.txt"
        for document in documents
    )


def test_search_finds_python_information():
    results = search_documents(
        "What programming language does the team use?"
    )

    assert len(results) > 0
    assert any("Python" in result["text"] for result in results)


def test_chunks_overlap_correctly():
    words = [f"word{i}" for i in range(150)]
    text = " ".join(words)

    chunks = split_into_chunks(
        text, chunk_size=100, overlap=20
    )

    assert len(chunks) == 2
    assert len(chunks[0].split()) == 100
    assert len(chunks[1].split()) == 70
    assert chunks[0].split()[-20:] == chunks[1].split()[:20]


def test_invalid_chunk_settings_are_rejected():
    import pytest

    with pytest.raises(ValueError):
        split_into_chunks("some text", chunk_size=0)

    with pytest.raises(ValueError):
        split_into_chunks(
            "some text", chunk_size=10, overlap=10
        )


def test_irrelevant_question_returns_no_results():
    results = search_documents(
        "What is the recipe for chocolate cake?"
    )

    assert results == []
