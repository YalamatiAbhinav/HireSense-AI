
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200


def test_resume_history_endpoint():
    response = client.get("/resumes")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert "resumes" in data
    assert isinstance(data["resumes"], list)


def test_chat_rejects_empty_question():
    response = client.post(
        "/chat",
        data={
            "resume_id": "test-resume-id",
            "question": "   "
        }
    )

    assert response.status_code == 400