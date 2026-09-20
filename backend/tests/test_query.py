import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app

client = TestClient(app)


def test_health_check_endpoint():
    """Test GET /health returns 200 and expected status fields."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "vector_store_loaded" in data
    assert "ollama_connected" in data
    assert "total_documents_indexed" in data


def test_query_invalid_empty_input():
    """Test POST /query with an empty question returns 422 Unprocessable Entity."""
    response = client.post("/query", json={"question": "   "})
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_query_missing_field():
    """Test POST /query with missing 'question' field returns 422 Unprocessable Entity."""
    response = client.post("/query", json={})
    assert response.status_code == 422


@patch("app.services.generation.generation_service.generate_answer", new_callable=AsyncMock)
@patch("app.services.retrieval.retrieval_service.retrieve_chunks")
def test_query_happy_path(mock_retrieve, mock_generate):
    """Test POST /query with valid input returns grounded answer and source citations."""
    mock_retrieve.return_value = [
        {
            "text": "Virtual memory is a memory management technique that provides an idealized abstraction of storage.",
            "document": "CS101_Operating_Systems_Guide.pdf",
            "page": 4,
            "chunk_id": 12,
            "distance": 0.15
        }
    ]
    mock_generate.return_value = (
        "Virtual memory is a memory management technique providing idealized storage abstraction [CS101_Operating_Systems_Guide.pdf, Page 4].",
        [{"document": "CS101_Operating_Systems_Guide.pdf", "page": 4, "snippet": "Virtual memory..."}]
    )

    response = client.post("/query", json={"question": "What is virtual memory?"})
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "sources" in data
    assert len(data["sources"]) == 1
    assert data["sources"][0]["document"] == "CS101_Operating_Systems_Guide.pdf"
    assert data["sources"][0]["page"] == 4
