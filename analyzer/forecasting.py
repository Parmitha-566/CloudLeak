
import math
import pandas as pd


REQUIRED_COLUMNS = {"date", "cost"}
LOOKBACK_DAYS = 7
FORECAST_DAYS = 7


def forecast_costs(historical_df: pd.DataFrame) -> dict:
    """
    Forecast cloud expenditure for the next 7 days.

    Uses the average of the most recent 7 daily cost totals.
    Forecasts are estimates, not actual expenditure.
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

    # Aggregate all resources into daily expenditure totals.
    daily_costs = (
        data.groupby("date")["cost"]
        .sum()
        .sort_index()
    )

    if len(daily_costs) < LOOKBACK_DAYS:
        raise ValueError(
            "At least 7 days of historical data are required."
        )

    # Use the latest 7 available daily observations.
    recent_costs = daily_costs.tail(LOOKBACK_DAYS)

    average_daily_cost = float(recent_costs.mean())

    # Forecast the next 7 calendar days after the latest date.
    last_date = daily_costs.index.max()

    forecasts = []

    for day in range(1, FORECAST_DAYS + 1):
        forecast_date = last_date + pd.Timedelta(days=day)

        forecasts.append({
            "date": forecast_date.strftime("%Y-%m-%d"),
            "forecasted_cost": round(average_daily_cost, 2),
            "record_type": "forecast"
        })

    return {
        "forecast_method": "7-day moving average",
        "historical_observations_used": len(recent_costs),
        "average_daily_cost": round(average_daily_cost, 2),
        "total_forecasted_cost": round(
            average_daily_cost * FORECAST_DAYS, 2
        ),
        "forecast_days": FORECAST_DAYS,
        "forecasts": forecasts,
        "disclaimer": (
            "These values are estimates based on historical "
            "expenditure, not actual future costs."
        )
    }
