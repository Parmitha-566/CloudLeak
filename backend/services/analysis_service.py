
from analyzer.recommendations import (
    generate_recommendations as analyzer_generate_recommendations,
)
from analyzer.anomaly_detection import (
    detect_anomalies as analyzer_detect_anomalies,
)
from analyzer.forecasting import forecast_costs

from backend.services.data_service import (
    get_analyzer_resource_dataframe,
    get_historical_anomaly_dataframe,
    get_historical_forecast_dataframe,
)


def generate_recommendations():
    """
    Generate recommendations using Member 2's actual analyzer.

    Savings estimates are produced by the analyzer.
    Priority is an application-level display label.
    """
    resource_df = get_analyzer_resource_dataframe()

    result = analyzer_generate_recommendations(resource_df)

    recommendations = []

    for item in result["recommendations"]:
        action = item["recommended_action"]

        if action == "investigate_stopping":
            recommendation_type = "Stop Resource Investigation"
            priority = "high"

        elif action == "consider_downsizing":
            recommendation_type = "Rightsizing"
            priority = "medium"

        else:
            recommendation_type = str(action)
            priority = "low"

        recommendations.append({
            "resource_id": str(item["resource_id"]),
            "recommendation_type": recommendation_type,
            "description": str(item["reason"]),
            "estimated_monthly_savings": round(
                float(item["estimated_monthly_savings"]), 2
            ),
            "priority": priority,
        })

    return recommendations


def detect_anomalies():
    """
    Detect unusual historical provider-level cost increases.

    Historical data is provider-level, so resource_id in the
    existing API response represents a provider identifier.
    Severity is a presentation label derived from the
    detected percentage increase, not a Member 2 model output.
    """
    historical_df = get_historical_anomaly_dataframe()

    result = analyzer_detect_anomalies(historical_df)

    anomalies = []

    for item in result["anomalies"]:
        increase = float(item["increase_percentage"])

        if increase >= 100:
            severity = "high"
        elif increase >= 50:
            severity = "medium"
        else:
            severity = "low"

        anomaly_date = item["date"]

        if hasattr(anomaly_date, "date"):
            anomaly_date = anomaly_date.date()

        if hasattr(anomaly_date, "isoformat"):
            anomaly_date = anomaly_date.isoformat()
        else:
            anomaly_date = str(anomaly_date)

        anomalies.append({
            "resource_id": str(item["resource_id"]),
            "date": anomaly_date,
            "observed_cost": round(float(item["actual_cost"]), 2),
            "expected_cost": round(float(item["baseline_cost"]), 2),
            "deviation_percentage": round(increase, 2),
            "severity": severity,
        })

    return anomalies


def generate_forecast(days=7):
    """
    Generate a seven-day expenditure forecast using Member 2.

    The integrated forecasting function currently supports
    a fixed seven-day forecast.
    """
    if days != 7:
        raise ValueError(
            "The integrated forecasting module supports exactly 7 days."
        )

    historical_df = get_historical_forecast_dataframe()

    result = forecast_costs(historical_df)

    forecast = []

    for item in result["forecasts"]:
        forecast_date = item["date"]

        if hasattr(forecast_date, "date"):
            forecast_date = forecast_date.date()

        if hasattr(forecast_date, "isoformat"):
            forecast_date = forecast_date.isoformat()
        else:
            forecast_date = str(forecast_date)

        forecast.append({
            "date": forecast_date,
            "predicted_cost": round(
                float(item["forecasted_cost"]), 2
            ),
            # Member 2 provides point forecasts, not confidence intervals.
            "lower_bound": None,
            "upper_bound": None,
        })

    return forecast
