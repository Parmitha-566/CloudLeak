
from pathlib import Path

import pandas as pd

from Member1.collector.data_loader import (
    load_billing_data,
    load_historical_costs,
)
from analyzer.cost_analysis import get_cost_summary


# Project root: CLOUDLEAK/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

BILLING_FILE = PROJECT_ROOT / "Member1" / "sample_billing.csv"
HISTORICAL_FILE = PROJECT_ROOT / "Member1" / "historical_costs.csv"


def get_billing_dataframe():
    """Load validated resource billing data from Member 1."""
    return load_billing_data(BILLING_FILE)


def get_historical_dataframe():
    """Load validated daily provider-level historical costs."""
    return load_historical_costs(HISTORICAL_FILE)


def get_analyzer_resource_dataframe():
    """
    Transform Member 1 resource data into Member 2's
    required cost-analysis input format.
    """
    df = get_billing_dataframe()

    analyzer_df = pd.DataFrame({
        "resource_id": df["resource_id"],
        "resource_type": df["resource_type"],
        "cost": df["monthly_cost_usd"],
        "utilization": (
            df["cpu_utilization_pct"]
            + df["memory_utilization_pct"]
        ) / 2,
    })

    return analyzer_df.reset_index(drop=True)


def get_historical_anomaly_dataframe():
    """
    Transform historical provider-level costs into
    Member 2's anomaly detector input format.

    Provider names are used as identifiers because
    Member 1's historical data is provider-level,
    not resource-level.
    """
    df = get_historical_dataframe()

    return pd.DataFrame({
        "date": df["date"],
        "resource_id": df["provider"],
        "cost": df["daily_cost_usd"],
    })


def get_historical_forecast_dataframe():
    """
    Aggregate daily costs across all providers.

    This produces one total expenditure record per day
    for Member 2's forecasting function.
    """
    df = get_historical_dataframe()

    daily_totals = (
        df.groupby("date", as_index=False)["daily_cost_usd"]
        .sum()
        .rename(columns={"daily_cost_usd": "cost"})
        .sort_values("date")
    )

    return daily_totals.reset_index(drop=True)


def get_cost_analysis():
    """Run Member 2's actual cost summary analysis."""
    analyzer_df = get_analyzer_resource_dataframe()
    return get_cost_summary(analyzer_df)


def get_resources():
    """Return actual resource records in the existing API format."""
    df = get_billing_dataframe()

    resources = []

    for _, row in df.iterrows():
        utilization = round(
            (
                float(row["cpu_utilization_pct"])
                + float(row["memory_utilization_pct"])
            ) / 2,
            2,
        )

        resources.append({
            "resource_id": str(row["resource_id"]),
            "resource_type": str(row["resource_type"]),
            "region": str(row["region"]),
            # Backward-compatible field: average utilization (%).
            "usage": utilization,
            "cost": round(float(row["monthly_cost_usd"]), 2),
            "utilization": utilization,
        })

    return resources


def get_total_cost():
    """Return total monthly resource expenditure in USD."""
    return get_cost_analysis()["total_monthly_expenditure"]


def get_resource_count():
    """Return the number of validated cloud resources."""
    return len(get_billing_dataframe())


def get_average_cost():
    """Return average monthly cost per resource."""
    count = get_resource_count()

    if count == 0:
        return 0.0

    return round(get_total_cost() / count, 2)


def get_cost_breakdown(field):
    """Group monthly resource expenditure by type or region."""
    if field not in {"resource_type", "region"}:
        raise ValueError(
            "Breakdown field must be resource_type or region."
        )

    df = get_billing_dataframe()

    grouped = (
        df.groupby(field)["monthly_cost_usd"]
        .sum()
        .sort_index()
    )

    return [
        {
            "name": str(name),
            "cost": round(float(cost), 2),
        }
        for name, cost in grouped.items()
    ]


def get_mock_anomalies():
    """
    Legacy compatibility function.

    Real anomaly detection will be connected in analysis_service.py.
    """
    return []
