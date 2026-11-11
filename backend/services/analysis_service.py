
from datetime import date, timedelta

from backend.services.data_service import (
    get_resources,
    get_total_cost,
    get_mock_anomalies
)


def generate_recommendations():
    """
    Generate simulated cost optimization recommendations
    based on resource utilization.
    """

    recommendations = []

    for resource in get_resources():

        utilization = resource["utilization"]
        resource_id = resource["resource_id"]

        # Identify underutilized resources
        if utilization < 40:

            savings = round(resource["cost"] * 0.30, 2)

            recommendations.append({
                "resource_id": resource_id,
                "recommendation_type": "Rightsizing",
                "description": (
                    "Resource utilization is low. "
                    "Consider using a smaller resource configuration."
                ),
                "estimated_monthly_savings": savings,
                "priority": "high"
            })

        # Identify heavily utilized resources
        elif utilization > 85:

            recommendations.append({
                "resource_id": resource_id,
                "recommendation_type": "Performance Optimization",
                "description": (
                    "Resource utilization is very high. "
                    "Review capacity to avoid performance issues."
                ),
                "estimated_monthly_savings": 0.0,
                "priority": "medium"
            })

    return recommendations


def detect_anomalies():
    """
    Return simulated cloud cost anomalies.
    """

    return get_mock_anomalies()


def generate_forecast(days=7):
    """
    Generate a simple seven-day simulated cost forecast.

    This is a baseline projection, not a trained
    machine learning forecasting model.
    """

    if days < 1:
        raise ValueError("Forecast days must be at least 1.")

    total_cost = get_total_cost()

    # Use the simulated monthly cost to estimate daily expenditure
    daily_cost = total_cost / 30

    forecast = []

    for day in range(1, days + 1):

        forecast_date = date.today() + timedelta(days=day)

        # Apply a small deterministic daily variation
        trend_factor = 1 + (0.01 * day)

        predicted_cost = round(
            daily_cost * trend_factor, 2
        )

        lower_bound = round(predicted_cost * 0.90, 2)
        upper_bound = round(predicted_cost * 1.10, 2)

        forecast.append({
            "date": forecast_date.isoformat(),
            "predicted_cost": predicted_cost,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound
        })

    return forecast
