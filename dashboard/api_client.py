
"""Live API client for the CLOUDLEAK Streamlit dashboard."""

import os
from typing import Any

import requests

DEFAULT_API_URL = os.getenv(
    "CLOUDLEAK_API_URL",
    "http://localhost:8006"
).rstrip("/")

DATA_MODE = os.getenv("CLOUDLEAK_DATA_MODE", "api").strip().lower()
REQUEST_TIMEOUT = 10


class APIError(RuntimeError):
    """Raised when the CLOUDLEAK API cannot provide valid data."""


def _get_json(endpoint: str) -> Any:
    url = f"{DEFAULT_API_URL}/api/{endpoint.lstrip('/')}"

    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()

    except requests.RequestException as exc:
        raise APIError(f"Could not retrieve {url}: {exc}") from exc

    except ValueError as exc:
        raise APIError(f"The API returned invalid JSON from {url}.") from exc


def _unwrap(payload: Any, key: str) -> Any:
    """Extract data from the backend's wrapped response."""
    if isinstance(payload, dict) and key in payload:
        return payload[key]
    return payload


def get_summary() -> dict:
    payload = _get_json("summary")
    payload = _unwrap(payload, "summary")

    if not isinstance(payload, dict):
        raise APIError("Invalid summary response.")

    return payload


def get_resources() -> list:
    payload = _get_json("resources")
    payload = _unwrap(payload, "resources")

    if not isinstance(payload, list):
        raise APIError("Invalid resources response.")

    return payload


def get_recommendations() -> list:
    payload = _get_json("recommendations")
    payload = _unwrap(payload, "recommendations")

    if not isinstance(payload, list):
        raise APIError("Invalid recommendations response.")

    return payload


def get_anomalies() -> list:
    payload = _get_json("anomalies")
    payload = _unwrap(payload, "anomalies")

    if not isinstance(payload, list):
        raise APIError("Invalid anomalies response.")

    return payload


def get_forecast() -> list:
    payload = _get_json("forecast")
    payload = _unwrap(payload, "forecast")

    if isinstance(payload, dict):
        payload = payload.get("forecast", [])

    if not isinstance(payload, list):
        raise APIError("Invalid forecast response.")

    return payload


def mock_dashboard_data():
    """Small fictional dataset retained for isolated unit tests."""

    resources = [
        {
            "resource_id": "demo-compute-01",
            "resource_type": "Compute",
            "region": "demo-region",
            "usage": 2.0,
            "cost": 100.0,
            "utilization": 10.0,
        },
        {
            "resource_id": "demo-database-01",
            "resource_type": "Database",
            "region": "demo-region",
            "usage": 4.0,
            "cost": 200.0,
            "utilization": 60.0,
        },
    ]

    recommendations = [
        {
            "resource_id": "demo-compute-01",
            "recommendation_type": "consider_downsizing",
            "description": "Demo recommendation only.",
            "estimated_savings": 30.0,
            "priority": "Medium",
        },
        {
            "resource_id": "demo-database-01",
            "recommendation_type": "investigate",
            "description": "Demo recommendation only.",
            "estimated_savings": 10.0,
            "priority": "Low",
        },
    ]

    anomalies = [
        {
            "resource_id": "demo-compute-01",
            "date": "2026-11-08",
            "increase_percent": 20.0,
            "description": "Fictional demonstration anomaly.",
            "severity": "Medium",
        }
    ]

    forecast = [
        {
            "date": f"2026-11-{day:02d}",
            "predicted_cost": 40.0 + day,
        }
        for day in range(15, 22)
    ]

    summary = {
        "total_monthly_expenditure": 300.0,
        "total_resources": len(resources),
        "average_cpu_utilization": 35.0,
        "estimated_potential_savings": 40.0,
        "currency": "USD",
    }

    return summary, resources, recommendations, anomalies, forecast


def load_dashboard_data(mode: str | None = None):
    """Return summary, resources, recommendations, anomalies, forecast, label."""

    selected_mode = (mode or DATA_MODE or "api").lower()

    if selected_mode == "mock":
        return (*mock_dashboard_data(), "MOCK DATA — FICTIONAL")

    if selected_mode not in {"api", "auto"}:
        raise APIError(f"Unsupported data mode: {selected_mode}")

    try:
        summary = get_summary()
        resources = get_resources()
        recommendations = get_recommendations()
        anomalies = get_anomalies()
        forecast = get_forecast()

        return (
            summary,
            resources,
            recommendations,
            anomalies,
            forecast,
            "LIVE API — CLOUDLEAK",
        )

    except APIError:
        if selected_mode == "api":
            raise

        return (
            *mock_dashboard_data(),
            "MOCK DATA — API UNAVAILABLE",
        )
