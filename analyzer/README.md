# CLOUDLEAK – Cost Analysis & Optimization Module

## 1. Overview

The Cost Analysis and Optimization module is responsible for analyzing cloud resource expenditure, detecting unusual cost increases, forecasting future costs, and generating resource optimization recommendations.

It is implemented in Python using Pandas and statistical techniques.

## 2. Module Structure

The `analyzer/` directory contains four main modules:

| File | Responsibility |
|---|---|
| `cost_analysis.py` | Calculates expenditure and resource utilization |
| `anomaly_detection.py` | Detects unusual cloud cost increases |
| `forecasting.py` | Forecasts expenditure for the next seven days |
| `recommendations.py` | Generates resource optimization suggestions |

## 3. Cost Analysis

**File:** `cost_analysis.py`

**Function:** `get_cost_summary(df)`

Responsibilities:
- Calculate total expenditure.
- Calculate expenditure by resource type.
- Calculate average resource utilization.
- Identify underutilized resources.

Underutilization threshold: 20%.

Required input columns:
- `resource_id`
- `resource_type`
- `cost`
- `utilization`

The function returns a dictionary containing expenditure statistics and underutilized resource details.

## 4. Anomaly Detection

**File:** `anomaly_detection.py`

**Function:** `detect_anomalies(historical_df)`

Responsibilities:
- Analyze historical cloud expenditure.
- Identify unusual cost increases.
- Compare recent costs against a historical baseline.
- Provide explanations for detected anomalies.

Detection approach:
- Uses a rolling historical window of seven observations.
- Calculates a median baseline.
- Uses Median Absolute Deviation (MAD) for robust variation estimation.
- Applies a minimum relative and absolute increase threshold.

Required input columns:
- `date`
- `resource_id`
- `cost`

The output includes the anomaly count, actual cost, baseline cost, threshold, percentage increase, and detection reason.

## 5. Cost Forecasting

**File:** `forecasting.py`

**Function:** `forecast_costs(historical_df)`

Responsibilities:
- Analyze historical daily expenditure.
- Estimate expenditure for the next seven days.
- Provide a daily forecast and total forecasted expenditure.

Forecasting approach:

Uses a seven-day moving average of the latest seven available daily cost observations.

Required input columns:
- `date`
- `cost`

The output includes:
- Forecast method.
- Historical observations used.
- Average daily cost.
- Total forecasted cost.
- Seven daily forecast records.

Forecast values are estimates, not actual expenditure.

## 6. Optimization Recommendations

**File:** `recommendations.py`

**Function:** `generate_recommendations(df)`

Responsibilities:
- Identify resources with low utilization.
- Suggest resources for downsizing or stopping investigation.
- Estimate potential monthly savings.
- Explain why each resource was selected.

Recommendation thresholds:

| Condition | Suggested action | Estimated savings assumption |
|---|---|---:|
| Utilization ≤ 5% | Investigate stopping | 80% |
| Utilization > 5% and < 20% | Consider downsizing | 30% |
| Utilization ≥ 20% | No recommendation from these rules | — |

Required input columns:
- `resource_id`
- `resource_type`
- `cost`
- `utilization`

Savings are heuristic estimates based on current resource costs. Actual savings depend on workload requirements, pricing, and operational constraints.

## 7. Input Validation and Error Handling

The modules validate:
- DataFrame input type.
- Required column availability.
- Missing identifiers and values.
- Numeric and finite cost values.
- Non-negative costs.
- Utilization values between 0 and 100.
- Valid date values.
- Minimum historical observations for forecasting.

Invalid inputs raise appropriate exceptions rather than silently producing misleading results.

## 8. Testing

Test file: `tests/test_analyzer.py`

The tests cover:
- Cost summary calculations.
- Missing and empty input handling.
- Anomaly detection.
- Normal cost behavior.
- Seven-day forecasting.
- Forecast input validation.
- Recommendation generation.
- Invalid utilization values.
- JSON serialization of results.

Run analyzer tests:

```powershell
python -m pytest tests/test_analyzer.py -v
```

Run the complete project test suite:

```powershell
python -m pytest -v
```

## 9. Limitations

- Forecasting uses a simple moving-average baseline and does not use a trained machine-learning model.
- Anomaly detection uses statistical thresholds and may not identify every unusual event.
- Optimization savings are estimates, not guaranteed savings.
- Input data quality and cost granularity affect the accuracy of results.
- Historical data must contain sufficient observations for forecasting and anomaly detection.

## 10. Integration Contract

The module exposes the following functions for use by the backend:

```python
get_cost_summary(df)
detect_anomalies(historical_df)
forecast_costs(historical_df)
generate_recommendations(df)
```

The functions accept Pandas DataFrames and return dictionaries or lists suitable for JSON serialization.

The shared input column names and cost units must be agreed upon with the data collector before integration.

---

**Project:** CLOUDLEAK – Intelligent Cloud Cost Optimization Platform

**Component:** Member 2 – Cost Analysis & Optimization Engineer