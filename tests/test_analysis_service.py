
import pytest

from backend.services.analysis_service import (
    generate_recommendations,
    detect_anomalies,
    generate_forecast,
)


def test_generate_recommendations():
    recommendations = generate_recommendations()

    assert isinstance(recommendations, list)
    assert len(recommendations) > 0

    for item in recommendations:
        assert "resource_id" in item
        assert "recommendation_type" in item
        assert "description" in item
        assert "estimated_monthly_savings" in item
        assert "priority" in item

        assert item["estimated_monthly_savings"] >= 0
        assert item["priority"] in ["high", "medium", "low"]


def test_detect_anomalies():
    anomalies = detect_anomalies()

    assert isinstance(anomalies, list)

    # Zero anomalies is valid when the detector finds no unusual costs.
    for item in anomalies:
        assert "resource_id" in item
        assert "date" in item
        assert "observed_cost" in item
        assert "expected_cost" in item
        assert "deviation_percentage" in item
        assert "severity" in item


def test_generate_forecast():
    forecast = generate_forecast(days=7)

    assert isinstance(forecast, list)
    assert len(forecast) == 7

    for item in forecast:
        assert "date" in item
        assert "predicted_cost" in item
        assert "lower_bound" in item
        assert "upper_bound" in item
        assert item["predicted_cost"] >= 0
        assert item["lower_bound"] is None
        assert item["upper_bound"] is None


def test_generate_forecast_invalid_days():
    with pytest.raises(ValueError):
        generate_forecast(days=0)


def test_generate_forecast_unsupported_days():
    with pytest.raises(ValueError):
        generate_forecast(days=14)
