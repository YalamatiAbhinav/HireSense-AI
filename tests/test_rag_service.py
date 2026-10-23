

from unittest.mock import patch

from backend.services.rag_service import (
    chunk_text,
    retrieve_resume_context
)


# ==========================================
# TEST 1: TEXT CHUNKING
# ==========================================

def test_chunk_text_creates_chunks():

    text = " ".join(["Python"] * 1500)

    chunks = chunk_text(
        text,
        chunk_size=700,
        overlap=100
    )

    assert len(chunks) == 3
    assert all(chunk.strip() for chunk in chunks)


# ==========================================
# TEST 2: EMPTY TEXT VALIDATION
# ==========================================

def test_chunk_text_rejects_empty_text():

    try:
        chunk_text("")

        assert False, "Expected ValueError"

    except ValueError:
        assert True


# ==========================================
# TEST 3: RAG CONTEXT RETRIEVAL
# ==========================================

@patch("backend.services.rag_service.create_embedding")
@patch("backend.services.rag_service.collection")
def test_retrieve_resume_context(mock_collection, mock_embedding):

    # Mock embedding generation
    mock_embedding.return_value = [0.1, 0.2, 0.3]

    # Mock vector database document count
    mock_collection.count.return_value = 5

    # Mock vector database search results
    mock_collection.query.return_value = {
        "documents": [
            ["Python developer with SQL experience."]
        ]
    }

    # Retrieve resume context
    context = retrieve_resume_context(
        "test-resume-id",
        "What are my skills?"
    )

    # Verify retrieved context
    assert "Python" in context
    assert "SQL" in context

    # Verify vector database was queried
    mock_collection.query.assert_called_once()
