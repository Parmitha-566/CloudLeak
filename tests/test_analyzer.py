
import json
import pandas as pd
import pytest

from analyzer.cost_analysis import get_cost_summary
from analyzer.anomaly_detection import detect_anomalies
from analyzer.forecasting import forecast_costs
from analyzer.recommendations import generate_recommendations


@pytest.fixture
def resource_data():
    return pd.DataFrame([
        {
            "resource_id": "EC2-001",
            "resource_type": "EC2",
            "cost": 100,
            "utilization": 80
        },
        {
            "resource_id": "EC2-002",
            "resource_type": "EC2",
            "cost": 200,
            "utilization": 10
        },
        {
            "resource_id": "S3-001",
            "resource_type": "S3",
            "cost": 50,
            "utilization": 4
        }
    ])


@pytest.fixture
def historical_data():
    return pd.DataFrame([
        {
            "date": f"2026-10-{day:02d}",
            "resource_id": "EC2-001",
            "cost": 100
        }
        for day in range(1, 8)
    ] + [{
        "date": "2026-10-08",
        "resource_id": "EC2-001",
        "cost": 250
    }])


def test_cost_summary(resource_data):
    result = get_cost_summary(resource_data)

    assert result["total_monthly_expenditure"] == 350.0
    assert result["average_utilization"] == 31.33
    assert result["underutilized_count"] == 2
    assert result["cost_by_resource_type"]["EC2"] == 300.0


def test_cost_summary_rejects_empty_data():
    with pytest.raises(ValueError):
        get_cost_summary(pd.DataFrame())


def test_cost_summary_rejects_missing_columns():
    df = pd.DataFrame({"cost": [100]})

    with pytest.raises(ValueError):
        get_cost_summary(df)


def test_anomaly_detection_finds_unusual_cost(historical_data):
    result = detect_anomalies(historical_data)

    assert result["anomaly_count"] == 1
    assert result["anomalies"][0]["resource_id"] == "EC2-001"
    assert result["anomalies"][0]["actual_cost"] == 250.0


def test_anomaly_detection_finds_no_anomaly():
    df = pd.DataFrame([
        {
            "date": f"2026-10-{day:02d}",
            "resource_id": "EC2-001",
            "cost": 100
        }
        for day in range(1, 9)
    ])

    result = detect_anomalies(df)

    assert result["anomaly_count"] == 0
    assert result["anomalies"] == []


def test_forecast_returns_seven_days():
    df = pd.DataFrame([
        {
            "date": f"2026-10-{day:02d}",
            "cost": 100 + (day - 1) * 10
        }
        for day in range(1, 8)
    ])

    result = forecast_costs(df)

    assert result["forecast_days"] == 7
    assert len(result["forecasts"]) == 7
    assert result["average_daily_cost"] == 130.0
    assert result["total_forecasted_cost"] == 910.0
    assert result["forecasts"][0]["date"] == "2026-10-08"
    assert result["forecasts"][0]["record_type"] == "forecast"


def test_forecast_rejects_insufficient_history():
    df = pd.DataFrame([
        {"date": "2026-10-01", "cost": 100},
        {"date": "2026-10-02", "cost": 110}
    ])

    with pytest.raises(ValueError):
        forecast_costs(df)


def test_recommendations(resource_data):
    result = generate_recommendations(resource_data)

    assert result["recommendation_count"] == 2
    assert result["total_estimated_monthly_savings"] == 100.0

    actions = {
        item["resource_id"]: item["recommended_action"]
        for item in result["recommendations"]
    }

    assert actions["EC2-002"] == "consider_downsizing"
    assert actions["S3-001"] == "investigate_stopping"


def test_recommendations_reject_invalid_utilization():
    df = pd.DataFrame([
        {
            "resource_id": "EC2-001",
            "resource_type": "EC2",
            "cost": 100,
            "utilization": 150
        }
    ])

    with pytest.raises(ValueError):
        generate_recommendations(df)


def test_analysis_results_are_json_serializable(resource_data):
    cost_result = get_cost_summary(resource_data)
    recommendation_result = generate_recommendations(resource_data)

    json.dumps(cost_result)
    json.dumps(recommendation_result)
