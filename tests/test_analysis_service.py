
import pytest

from backend.services.analysis_service import (
    generate_recommendations,
    detect_anomalies,
    generate_forecast
)


def test_generate_recommendations():
    recommendations = generate_recommendations()

    assert isinstance(recommendations, list)
    assert len(recommendations) == 3

    for item in recommendations:
        assert "resource_id" in item
        assert "recommendation_type" in item
        assert "estimated_monthly_savings" in item


def test_detect_anomalies():
    anomalies = detect_anomalies()

    assert isinstance(anomalies, list)
    assert len(anomalies) == 2

    for item in anomalies:
        assert "observed_cost" in item
        assert "expected_cost" in item
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


def test_generate_forecast_invalid_days():
    with pytest.raises(ValueError):
        generate_forecast(days=0)
