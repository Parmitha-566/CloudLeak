
from backend.services import data_service, analysis_service
from datetime import datetime

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

    # Confirm that the timestamp is valid ISO 8601
    datetime.fromisoformat(data["timestamp"])


def test_summary_endpoint():
    response = client.get("/api/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["total_cost"] >= 0
    assert data["resource_count"] == 5
    assert data["average_cost"] >= 0
    assert data["currency"] == "USD"
    assert 0 <= data["average_utilization"] <= 100
    assert data["high_utilization_resources"] >= 0

    assert isinstance(data["service_breakdown"], list)
    assert isinstance(data["region_breakdown"], list)


def test_resources_endpoint():
    response = client.get("/api/resources")

    assert response.status_code == 200

    data = response.json()

    assert data["total_resources"] == 5
    assert len(data["resources"]) == 5

    for resource in data["resources"]:
        assert "resource_id" in resource
        assert "resource_type" in resource
        assert "region" in resource
        assert "usage" in resource
        assert "cost" in resource
        assert "utilization" in resource


def test_recommendations_endpoint():
    response = client.get("/api/recommendations")

    assert response.status_code == 200

    data = response.json()

    assert data["total_recommendations"] == 3
    assert len(data["recommendations"]) == 3

    for recommendation in data["recommendations"]:
        assert "resource_id" in recommendation
        assert "recommendation_type" in recommendation
        assert "description" in recommendation
        assert "estimated_monthly_savings" in recommendation
        assert "priority" in recommendation


def test_anomalies_endpoint():
    response = client.get("/api/anomalies")

    assert response.status_code == 200

    data = response.json()

    assert data["total_anomalies"] == 2
    assert len(data["anomalies"]) == 2

    for anomaly in data["anomalies"]:
        assert "resource_id" in anomaly
        assert "date" in anomaly
        assert "observed_cost" in anomaly
        assert "expected_cost" in anomaly
        assert "deviation_percentage" in anomaly
        assert "severity" in anomaly


def test_forecast_endpoint():
    response = client.get("/api/forecast")

    assert response.status_code == 200

    data = response.json()

    assert data["forecast_period_days"] == 7
    assert data["currency"] == "USD"
    assert len(data["forecast"]) == 7

    for record in data["forecast"]:
        assert "date" in record
        assert "predicted_cost" in record
        assert "lower_bound" in record
        assert "upper_bound" in record

        assert record["predicted_cost"] >= 0
        assert record["lower_bound"] <= record["predicted_cost"]
        assert record["upper_bound"] >= record["predicted_cost"]


def test_swagger_documentation():
    response = client.get("/docs")

    assert response.status_code == 200


def test_openapi_schema():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    schema = response.json()
    paths = schema["paths"]

    expected_endpoints = [
        "/api/health",
        "/api/summary",
        "/api/resources",
        "/api/recommendations",
        "/api/anomalies",
        "/api/forecast"
    ]

    for endpoint in expected_endpoints:
        assert endpoint in paths
        assert "get" in paths[endpoint]


def test_summary_handles_internal_error(monkeypatch):
    def mock_failure():
        raise RuntimeError("Simulated database failure")

    monkeypatch.setattr(
        data_service,
        "get_resources",
        mock_failure
    )

    response = client.get("/api/summary")

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "Internal server error while generating summary."
    )


def test_resources_handles_internal_error(monkeypatch):
    def mock_failure():
        raise RuntimeError("Simulated data failure")

    monkeypatch.setattr(
        data_service,
        "get_resources",
        mock_failure
    )

    response = client.get("/api/resources")

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "Internal server error while retrieving resources."
    )


def test_recommendations_handles_internal_error(monkeypatch):
    def mock_failure():
        raise RuntimeError("Simulated analysis failure")

    monkeypatch.setattr(
        analysis_service,
        "generate_recommendations",
        mock_failure
    )

    response = client.get("/api/recommendations")

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "Internal server error while generating recommendations."
    )


def test_anomalies_handles_internal_error(monkeypatch):
    def mock_failure():
        raise RuntimeError("Simulated anomaly failure")

    monkeypatch.setattr(
        analysis_service,
        "detect_anomalies",
        mock_failure
    )

    response = client.get("/api/anomalies")

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "Internal server error while detecting anomalies."
    )


def test_forecast_handles_internal_error(monkeypatch):
    def mock_failure(days=7):
        raise RuntimeError("Simulated forecast failure")

    monkeypatch.setattr(
        analysis_service,
        "generate_forecast",
        mock_failure
    )

    response = client.get("/api/forecast")

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "Internal server error while generating forecast."
    )


def test_cors_preflight():
    response = client.options(
        "/api/health",
        headers={
            "Origin": "http://localhost:8501",
            "Access-Control-Request-Method": "GET"
        }
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == (
        "http://localhost:8501"
    )
    

def test_forecast_handles_invalid_value(monkeypatch):
    def mock_invalid_forecast(days=7):
        raise ValueError("Invalid forecast period")

    monkeypatch.setattr(
        analysis_service,
        "generate_forecast",
        mock_invalid_forecast
    )

    response = client.get("/api/forecast")

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid forecast period"

