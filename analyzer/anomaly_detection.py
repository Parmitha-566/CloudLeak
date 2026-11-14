
import math
import pandas as pd


REQUIRED_COLUMNS = {"date", "resource_id", "cost"}

LOOKBACK_DAYS = 7
MAD_MULTIPLIER = 3.0
MINIMUM_RELATIVE_INCREASE = 0.50
MINIMUM_ABSOLUTE_INCREASE = 1.0


def detect_anomalies(historical_df: pd.DataFrame) -> dict:
    """
    Detect unusually high daily costs for each resource.

    Requires date, resource_id, and cost columns.
    Each observation is compared with the previous 7 observations.
    """

    if not isinstance(historical_df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame.")

    if historical_df.empty:
        raise ValueError("Historical data cannot be empty.")

    missing = REQUIRED_COLUMNS - set(historical_df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    data = historical_df.copy()

    if data["resource_id"].isna().any():
        raise ValueError("Resource IDs cannot contain missing values.")

    data["date"] = pd.to_datetime(
        data["date"], errors="coerce"
    )

    if data["date"].isna().any():
        raise ValueError("Dates must contain valid date values.")

    data["date"] = data["date"].dt.normalize()

    data["cost"] = pd.to_numeric(
        data["cost"], errors="coerce"
    )

    if data["cost"].isna().any():
        raise ValueError("Cost must contain valid numeric values.")

    if not data["cost"].map(math.isfinite).all():
        raise ValueError("Cost values must be finite.")

    if (data["cost"] < 0).any():
        raise ValueError("Cost cannot be negative.")

    # Aggregate multiple records for the same resource and date.
    daily = (
        data.groupby(["resource_id", "date"], as_index=False)["cost"]
        .sum()
        .sort_values(["resource_id", "date"])
    )

    anomalies = []

    for resource_id, group in daily.groupby("resource_id"):

        group = group.sort_values("date").reset_index(drop=True)

        # At least 7 previous observations are required.
        for index in range(LOOKBACK_DAYS, len(group)):

            previous_costs = group.loc[
                index - LOOKBACK_DAYS:index - 1, "cost"
            ]

            current = group.loc[index]

            baseline = float(previous_costs.median())

            # Median Absolute Deviation (MAD).
            mad = float(
                (previous_costs - baseline).abs().median()
            )

            robust_spread = MAD_MULTIPLIER * 1.4826 * mad

            # Fallback threshold when historical MAD is zero.
            fallback = max(
                baseline * MINIMUM_RELATIVE_INCREASE,
                MINIMUM_ABSOLUTE_INCREASE
            )

            threshold = baseline + max(
                robust_spread, fallback
            )

            actual_cost = float(current["cost"])

            if actual_cost > threshold:
                anomalies.append({
                    "resource_id": str(resource_id),
                    "date": current["date"].strftime("%Y-%m-%d"),
                    "actual_cost": round(actual_cost, 2),
                    "baseline_cost": round(baseline, 2),
                    "threshold": round(threshold, 2),
                    "increase_percentage": round(
                        ((actual_cost - baseline) / baseline * 100)
                        if baseline > 0 else 0.0,
                        2
                    ),
                    "reason": (
                        "Daily cost exceeded the statistical "
                        "anomaly threshold based on the previous "
                        "7 observations."
                    )
                })

    return {
        "anomaly_count": len(anomalies),
        "anomalies": anomalies
    }
