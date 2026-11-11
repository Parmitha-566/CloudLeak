
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Welcome to CLOUDLEAK API"
    assert data["documentation"] == "/docs"


def test_health_endpoint():
    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["project"] == "CLOUDLEAK"
    assert data["version"] == "1.0.0"
    assert "timestamp" in data
