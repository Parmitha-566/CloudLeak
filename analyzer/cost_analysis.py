
import math
import pandas as pd


REQUIRED_COLUMNS = {
    "resource_id",
    "resource_type",
    "cost",
    "utilization",
}

# Resources below this utilization are considered underutilized.
UNDERUTILIZATION_THRESHOLD = 20.0


def get_cost_summary(df: pd.DataFrame) -> dict:
    """
    Generate a cloud cost summary.

    Required columns:
    resource_id, resource_type, cost, utilization

    Returns total expenditure, cost by resource type,
    average utilization, and underutilized resources.
    """

    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if df.empty:
        raise ValueError("Input DataFrame cannot be empty.")

    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    data = df.copy()

    # Validate resource identifiers and types.
    if data["resource_id"].isna().any():
        raise ValueError("Resource IDs cannot contain missing values.")

    if data["resource_type"].isna().any():
        raise ValueError("Resource types cannot contain missing values.")

    # Convert numeric columns safely.
    for column in ["cost", "utilization"]:
        data[column] = pd.to_numeric(data[column], errors="coerce")

        if data[column].isna().any():
            raise ValueError(f"{column} must contain valid numeric values.")

        if not data[column].map(math.isfinite).all():
            raise ValueError(f"{column} must contain finite values.")

    if (data["cost"] < 0).any():
        raise ValueError("Cost cannot be negative.")

    if not data["utilization"].between(0, 100).all():
        raise ValueError("Utilization must be between 0 and 100.")

    # Calculate overall expenditure.
    total_expenditure = float(data["cost"].sum())

    # Calculate expenditure grouped by resource type.
    cost_by_resource_type = (
        data.groupby("resource_type")["cost"]
        .sum()
        .to_dict()
    )

    cost_by_resource_type = {
        str(resource_type): round(float(cost), 2)
        for resource_type, cost in cost_by_resource_type.items()
    }

    # Calculate average utilization.
    average_utilization = float(data["utilization"].mean())

    # Identify underutilized resources.
    underutilized = data[
        data["utilization"] < UNDERUTILIZATION_THRESHOLD
    ]

    underutilized_resources = []

    for _, resource in underutilized.iterrows():
        underutilized_resources.append({
            "resource_id": str(resource["resource_id"]),
            "resource_type": str(resource["resource_type"]),
            "cost": round(float(resource["cost"]), 2),
            "utilization": round(float(resource["utilization"]), 2),
            "reason": (
                f"Resource utilization is below "
                f"{UNDERUTILIZATION_THRESHOLD}%."
            ),
        })

    return {
        "total_monthly_expenditure": round(total_expenditure, 2),
        "cost_by_resource_type": cost_by_resource_type,
        "average_utilization": round(average_utilization, 2),
        "underutilized_count": len(underutilized_resources),
        "underutilized_resources": underutilized_resources,
    }
