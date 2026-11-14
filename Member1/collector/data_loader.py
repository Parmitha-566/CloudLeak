from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR


def load_billing_data(path=None):
    """Load and validate cloud billing resource data."""

    file_path = Path(path) if path else DATA_DIR / "sample_billing.csv"

    df = pd.read_csv(file_path)

    required = [
        "resource_id",
        "resource_type",
        "cpu_cores",
        "memory_gb",
        "cpu_utilization_pct",
        "memory_utilization_pct",
        "monthly_cost_usd",
        "region"
    ]

    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df = df[required].copy()

    numeric = [
        "cpu_cores",
        "memory_gb",
        "cpu_utilization_pct",
        "memory_utilization_pct",
        "monthly_cost_usd"
    ]

    for column in numeric:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(subset=[
        "resource_id", "resource_type", "region"
    ])

    df = df.dropna(subset=numeric)

    df = df.drop_duplicates(subset=["resource_id"])

    if (df["cpu_utilization_pct"].lt(0) |
        df["cpu_utilization_pct"].gt(100)).any():
        raise ValueError("Invalid CPU utilization.")

    if (df["memory_utilization_pct"].lt(0) |
        df["memory_utilization_pct"].gt(100)).any():
        raise ValueError("Invalid memory utilization.")

    if (df[numeric].lt(0)).any().any():
        raise ValueError("Negative numeric values are invalid.")

    return df.reset_index(drop=True)


def load_historical_costs(path=None):
    """Load and validate historical cloud costs."""

    file_path = (
        Path(path) if path
        else DATA_DIR / "historical_costs.csv"
    )

    df = pd.read_csv(file_path)

    required = [
        "date", "provider", "region",
        "currency", "daily_cost_usd"
    ]

    missing = set(required) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["daily_cost_usd"] = pd.to_numeric(
        df["daily_cost_usd"], errors="coerce"
    )

    df = df.dropna(subset=required)

    if df["daily_cost_usd"].lt(0).any():
        raise ValueError("Negative historical costs are invalid.")

    return df.reset_index(drop=True)