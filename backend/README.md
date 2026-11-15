# CLOUDLEAK – Backend API

## 1. Overview

The CLOUDLEAK Backend API provides REST endpoints for cloud cost monitoring, resource analysis, anomaly detection, optimization recommendations, and cost forecasting.

The backend is built using:
- Python
- FastAPI
- Pydantic
- Uvicorn
- Pandas and NumPy

The backend integrates the Member 1 billing data collector with the project's cost analysis and prediction modules.

## 2. Project Structure

```text
backend/
├── main.py
├── README.md
├── schemas/
│   └── response_models.py
├── services/
│   ├── analysis_service.py
│   └── data_service.py
└── utils/
    └── helpers.py
```

## 3. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/health | Checks backend availability |
| GET | /api/summary | Returns overall cost and resource metrics |
| GET | /api/resources | Returns cloud resource information |
| GET | /api/recommendations | Returns optimization recommendations |
| GET | /api/anomalies | Returns detected cost anomalies |
| GET | /api/forecast | Returns a seven-day cost forecast |

Interactive API documentation is available at `/docs`.

## 4. Data Integration

The backend uses the project billing datasets:

- `Member1/sample_billing.csv`
- `Member1/historical_costs.csv`

The data service loads and validates these datasets and prepares the information for the analyzer modules.

Resource utilization is calculated as the average of CPU and memory utilization percentages. This is an equal-weighted average used for analysis.

## 5. Cost Analysis and Recommendations

The analyzer evaluates resource costs and utilization.

Current recommendation rules:

- Utilization at or below 5%: investigate stopping the resource.
- Utilization above 5% and below 20%: consider downsizing.
- Utilization at or above 20%: no underutilization recommendation.

Estimated savings are based on assumptions and are not guaranteed savings.

## 6. Anomaly Detection

The anomaly detector analyzes historical daily costs.

It compares a cost observation with the previous seven available observations for the same identifier and uses a median and median absolute deviation (MAD) based baseline, with fallback thresholds.

The current historical dataset is grouped by cloud provider. Therefore, anomaly identifiers represent providers rather than individual cloud resources.

An empty anomaly response means no observations crossed the configured detection thresholds.

## 7. Cost Forecasting

The forecasting module uses the most recent seven daily expenditure observations.

It calculates the average daily cost and uses that value to forecast expenditure for the next seven calendar days.

Current limitations:
- Forecast horizon is fixed at seven days.
- The method is a moving-average baseline, not a machine-learning model.
- Confidence intervals are not calculated; lower and upper bounds are returned as null.
- At least seven historical observations are required.

## 8. Running the Backend Locally

From the project root:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Open:

- API: http://127.0.0.1:8000
- Swagger documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/api/health

## 9. Running Tests

From the project root:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

The backend is covered by unit and API integration tests in the project's `tests/` directory.

## 10. Docker and Kubernetes

The backend can be containerized using the root `Dockerfile` and run with Docker Compose.

Kubernetes deployment resources are maintained in the root `k8s/` directory. The backend is deployed as `cloudleak-backend` and exposed internally through a Kubernetes Service on port 8000.

## 11. Current Implementation Status

Implemented:
- FastAPI backend and six REST endpoints
- Billing and historical data integration
- Resource cost and utilization analysis
- Optimization recommendations
- Historical cost anomaly detection
- Seven-day expenditure forecasting
- Pydantic response models
- Automated tests
- Docker and Kubernetes deployment configuration
