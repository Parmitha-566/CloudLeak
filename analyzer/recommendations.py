
import math
import pandas as pd


REQUIRED_COLUMNS = {
    "resource_id",
    "resource_type",
    "cost",
    "utilization",
}

UNDERUTILIZATION_THRESHOLD = 20.0
STOP_THRESHOLD = 5.0

# Planning assumptions, not guaranteed savings.
DOWNSIZE_SAVINGS_RATE = 0.30
STOP_SAVINGS_RATE = 0.80


def generate_recommendations(df: pd.DataFrame) -> dict:
    """
    Generate cost optimization recommendations.

    Resources with utilization <= 5% are candidates
    for stopping or investigation.

    Resources with utilization > 5% and < 20% are
    candidates for downsizing.

    Savings are estimates based on stated assumptions.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if df.empty:
        raise ValueError("Input DataFrame cannot be empty.")

    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    data = df.copy()

    if data["resource_id"].isna().any():
        raise ValueError("Resource IDs cannot be missing.")

    if data["resource_type"].isna().any():
        raise ValueError("Resource types cannot be missing.")

    for column in ["cost", "utilization"]:
        data[column] = pd.to_numeric(
            data[column], errors="coerce"
        )

        if data[column].isna().any():
            raise ValueError(
                f"{column} must contain valid numeric values."
            )

        if not data[column].map(math.isfinite).all():
            raise ValueError(
                f"{column} must contain finite values."
            )

    if (data["cost"] < 0).any():
        raise ValueError("Cost cannot be negative.")

    if not data["utilization"].between(0, 100).all():
        raise ValueError(
            "Utilization must be between 0 and 100."
        )

    recommendations = []

    for _, resource in data.iterrows():

        utilization = float(resource["utilization"])
        monthly_cost = float(resource["cost"])

        if utilization <= STOP_THRESHOLD:
            action = "investigate_stopping"
            savings_rate = STOP_SAVINGS_RATE
            reason = (
                "Very low utilization. Investigate whether "
                "the resource can safely be stopped."
            )

        elif utilization < UNDERUTILIZATION_THRESHOLD:
            action = "consider_downsizing"
            savings_rate = DOWNSIZE_SAVINGS_RATE
            reason = (
                "Low utilization. Consider moving to a "
                "smaller resource configuration."
            )

        else:
            continue

        estimated_savings = monthly_cost * savings_rate

        recommendations.append({
            "resource_id": str(resource["resource_id"]),
            "resource_type": str(resource["resource_type"]),
            "current_monthly_cost": round(monthly_cost, 2),
            "utilization": round(utilization, 2),
            "recommended_action": action,
            "estimated_monthly_savings": round(
                estimated_savings, 2
            ),
            "reason": reason,
        })

    total_potential_savings = sum(
        item["estimated_monthly_savings"]
        for item in recommendations
    )

    return {
        "recommendation_count": len(recommendations),
        "total_estimated_monthly_savings": round(
            total_potential_savings, 2
        ),
        "assumptions": {
            "underutilization_threshold_percent": 20,
            "stop_candidate_threshold_percent": 5,
            "downsizing_savings_rate_percent": 30,
            "stopping_savings_rate_percent": 80,
        },
        "disclaimer": (
            "Savings are estimates based on assumptions. "
            "Actual savings depend on workload requirements, "
            "dependencies, pricing, and operational constraints. "
            "No resource should be stopped without verification."
        ),
        "recommendations": recommendations,
    }
