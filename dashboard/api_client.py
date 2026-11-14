"""API access and demo-data helpers for the CloudLeak dashboard."""
from __future__ import annotations

import os
from typing import Any

import requests

DEFAULT_API_URL = os.getenv("CLOUDLEAK_API_URL", "http://localhost:8000").rstrip("/")
DATA_MODE = os.getenv("CLOUDLEAK_DATA_MODE", "auto").strip().lower()


class APIError(RuntimeError):
    """Raised when a CloudLeak API request cannot be completed."""


def _get_json(endpoint: str, timeout: int = 5) -> Any:
    url = f"{DEFAULT_API_URL}/api/{endpoint.lstrip('/')}"
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise APIError(f"Could not retrieve {url}: {exc}") from exc
    except ValueError as exc:
        raise APIError(f"The API returned invalid JSON for {url}.") from exc


def _unwrap(payload: Any, key: str) -> Any:
    """Accept either a direct payload or a common {key: ...} wrapper."""
    if isinstance(payload, dict) and key in payload:
        return payload[key]
    return payload


def get_summary() -> dict:
    payload = _get_json("summary")
    payload = _unwrap(payload, "summary")
    if not isinstance(payload, dict):
        raise APIError("The /api/summary response must be a JSON object.")
    return payload


def get_resources() -> list[dict]:
    payload = _get_json("resources")
    payload = _unwrap(payload, "resources")
    if not isinstance(payload, list):
        raise APIError("The /api/resources response must be a JSON array.")
    return [item for item in payload if isinstance(item, dict)]


def get_recommendations() -> list[dict]:
    payload = _get_json("recommendations")
    payload = _unwrap(payload, "recommendations")
    if not isinstance(payload, list):
        raise APIError("The /api/recommendations response must be a JSON array.")
    return [item for item in payload if isinstance(item, dict)]


def get_anomalies() -> list[dict]:
    payload = _get_json("anomalies")
    payload = _unwrap(payload, "anomalies")
    if not isinstance(payload, list):
        raise APIError("The /api/anomalies response must be a JSON array.")
    return [item for item in payload if isinstance(item, dict)]


def get_forecast() -> list[dict]:
    payload = _get_json("forecast")
    payload = _unwrap(payload, "forecast")
    if isinstance(payload, dict):
        payload = payload.get("forecast", payload.get("predictions", []))
    if not isinstance(payload, list):
        raise APIError("The /api/forecast response must contain a JSON array.")
    return [item for item in payload if isinstance(item, dict)]


def load_dashboard_data(mode: str | None = None) -> tuple[dict, list, list, list, list, str]:
    """
    Return (summary, resources, recommendations, anomalies, forecast, source_label).

    mode='mock': always use demo data.
    mode='api': require live API responses.
    mode='auto': use API if all endpoints work; otherwise use demo data.
    """
    selected_mode = (mode or DATA_MODE or "auto").lower()
    if selected_mode not in {"mock", "api", "auto"}:
        selected_mode = "auto"

    if selected_mode == "mock":
        data = mock_dashboard_data()
        return (*data, "MOCK DATA")

    try:
        summary = get_summary()
        resources = get_resources()
        recommendations = get_recommendations()
        anomalies = get_anomalies()
        forecast = get_forecast()
        return summary, resources, recommendations, anomalies, forecast, "LIVE API"
    except APIError:
        if selected_mode == "api":
            raise
        data = mock_dashboard_data()
        return (*data, "MOCK DATA — API unavailable; showing demonstration data")


def mock_dashboard_data() -> tuple[dict, list, list, list, list]:
    """Clearly fictional sample data for UI development and demos."""
    resources = [
        {"resource_id": "compute-web-01", "resource_type": "Compute", "cpu_utilization": 12, "memory_utilization": 28, "monthly_cost": 145.00, "region": "us-east-1"},
        {"resource_id": "compute-api-02", "resource_type": "Compute", "cpu_utilization": 76, "memory_utilization": 68, "monthly_cost": 220.00, "region": "us-east-1"},
        {"resource_id": "database-01", "resource_type": "Database", "cpu_utilization": 19, "memory_utilization": 34, "monthly_cost": 310.00, "region": "ap-south-1"},
        {"resource_id": "storage-archive-01", "resource_type": "Storage", "cpu_utilization": 0, "memory_utilization": 0, "monthly_cost": 85.00, "region": "ap-south-1"},
        {"resource_id": "compute-worker-03", "resource_type": "Compute", "cpu_utilization": 9, "memory_utilization": 17, "monthly_cost": 175.00, "region": "eu-west-1"},
        {"resource_id": "database-analytics", "resource_type": "Database", "cpu_utilization": 82, "memory_utilization": 88, "monthly_cost": 390.00, "region": "eu-west-1"},
    ]
    total = sum(float(r["monthly_cost"]) for r in resources)
    avg_cpu = sum(float(r["cpu_utilization"]) for r in resources) / len(resources)
    recommendations = [
        {"resource_id": "compute-web-01", "action": "Consider downsizing", "reason": "CPU utilization has remained below 15% in the sample period.", "estimated_savings": 48.00, "priority": "High"},
        {"resource_id": "compute-worker-03", "action": "Schedule off-hours shutdown", "reason": "Low average CPU and memory utilization suggest intermittent demand.", "estimated_savings": 52.50, "priority": "Medium"},
        {"resource_id": "storage-archive-01", "action": "Review storage tier", "reason": "Move infrequently accessed data to a lower-cost storage tier if appropriate.", "estimated_savings": 17.00, "priority": "Low"},
    ]
    anomalies = [
        {"resource_id": "database-analytics", "date": "2026-11-08", "increase_percent": 31.5, "description": "Sample spend increased above its recent baseline.", "severity": "High"},
        {"resource_id": "compute-api-02", "date": "2026-11-06", "increase_percent": 14.2, "description": "Sample compute spend rose moderately compared with the previous period.", "severity": "Medium"},
    ]
    forecast = [
        {"date": "2026-11-10", "predicted_cost": 43.2},
        {"date": "2026-11-11", "predicted_cost": 44.0},
        {"date": "2026-11-12", "predicted_cost": 44.8},
        {"date": "2026-11-13", "predicted_cost": 45.1},
        {"date": "2026-11-14", "predicted_cost": 45.7},
        {"date": "2026-11-15", "predicted_cost": 46.3},
        {"date": "2026-11-16", "predicted_cost": 46.8},
    ]
    summary = {
        "total_monthly_expenditure": round(total, 2),
        "total_resources": len(resources),
        "average_cpu_utilization": round(avg_cpu, 1),
        "estimated_potential_savings": round(sum(r["estimated_savings"] for r in recommendations), 2),
        "currency": "USD",
    }
    return summary, resources, recommendations, anomalies, forecast
