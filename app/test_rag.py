
from rag import load_documents, search_documents


def test_documents_are_loaded():
    documents = load_documents()

    assert len(documents) > 0
    assert any(
        document["source"] == "company_info.txt"
        for document in documents
    )


def test_search_finds_python_information():
    results = search_documents("What programming language does the team use?")

    assert len(results) > 0
    assert any("Python" in result["text"] for result in results)
