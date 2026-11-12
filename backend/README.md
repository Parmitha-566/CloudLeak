
@'
# CLOUDLEAK – Backend API

## 1. Overview

The CLOUDLEAK Backend API provides REST endpoints for cloud cost monitoring, resource analysis, anomaly reporting, optimization recommendations, and cost forecasting.

The backend is developed using:
- Python
- FastAPI
- Pydantic
- Uvicorn

**Current development status:** The backend uses simulated cloud resource data for independent development. Integration with the actual cloud data collector and cost analyzer is planned for a later phase.

## 2. Project Structure

```text
backend/
├── __init__.py
├── main.py
├── schemas/
│   ├── __init__.py
│   └── response_models.py
├── services/
│   ├── __init__.py
│   ├── data_service.py
│   └── analysis_service.py
└── utils/
    └── __init__.py
```

### Main Components

- `main.py`: Initializes FastAPI, configures CORS, defines API routes, and handles errors.
- `services/data_service.py`: Supplies simulated resource data and calculates cost summaries.
- `services/analysis_service.py`: Generates recommendations, returns simulated anomalies, and produces baseline forecasts.
- `schemas/response_models.py`: Defines Pydantic response models and validates API output.

## 3. API Endpoints

Base URL:

```text
http://localhost:8000
```

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/api/health` | Backend health status |
| GET | `/api/summary` | Overall cloud cost summary |
| GET | `/api/resources` | Cloud resource records |
| GET | `/api/recommendations` | Optimization recommendations |
| GET | `/api/anomalies` | Detected/simulated cost anomalies |
| GET | `/api/forecast` | Seven-day cost forecast |

## 4. Endpoint Details

### GET `/api/health`

Returns the backend status, project name, version, and UTC timestamp.

Example:

```json
{
  "status": "healthy",
  "project": "CLOUDLEAK",
  "version": "1.0.0",
  "timestamp": "2026-11-12T10:00:00Z"
}
```

### GET `/api/summary`

Returns:
- Total cloud expenditure
- Number of resources
- Average cost per resource
- Currency
- Average resource utilization
- Number of highly utilized resources
- Cost breakdown by service type
- Cost breakdown by region

### GET `/api/resources`

Returns the total resource count and individual resource records.

Each resource contains:
- `resource_id`
- `resource_type`
- `region`
- `usage`
- `cost`
- `utilization`

### GET `/api/recommendations`

Generates recommendations using resource utilization:

- Below 40%: Suggests rightsizing, with estimated savings calculated as 30% of the resource cost.
- Above 85%: Suggests performance optimization and capacity review.
- Other utilization levels: No recommendation is currently generated.

These savings are estimates, not guaranteed savings.

### GET `/api/anomalies`

Returns simulated cost anomalies containing:
- Resource ID
- Date
- Observed cost
- Expected cost
- Deviation percentage
- Severity

The current implementation uses predefined demo anomaly records. It does not yet run a statistical anomaly-detection algorithm.

### GET `/api/forecast`

Returns a seven-day cost projection containing:
- Forecast date
- Predicted cost
- Lower bound
- Upper bound

The current forecast uses the total simulated resource cost divided by 30 as a daily baseline. A small deterministic daily increase is applied, with lower and upper bounds set at 10% below and above the prediction.

This is a baseline projection, not a trained machine-learning model.

## 5. Response Validation

Pydantic models in `schemas/response_models.py` validate API responses.

Examples of validation rules:
- Costs and usage values must be non-negative.
- Resource utilization must be between 0 and 100.
- Resource counts must be non-negative.
- Forecast duration must be at least one day.
- Dates and timestamps must use valid date/time formats.

## 6. Error Handling

The API uses HTTP status codes and structured error responses.

- `200`: Successful request.
- `400`: Invalid forecast request.
- `500`: Internal server error.

Exceptions are logged through Python's logging module. Internal error details are not exposed in generic server-error responses.

## 7. CORS Configuration

The backend currently allows requests from:

```text
http://localhost:8501
http://127.0.0.1:8501
```

Credentials, methods, and headers are enabled for these configured origins.

## 8. Running the Backend

Activate the project's virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies if required:

```powershell
python -m pip install -r requirements.txt
```

Start the API:

```powershell
uvicorn backend.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Interactive Swagger documentation:

```text
http://localhost:8000/docs
```

Alternative API documentation:

```text
http://localhost:8000/redoc
```

## 9. Testing

Run the backend API tests:

```powershell
python -m pytest tests/test_api.py -v
```

Run the complete project test suite:

```powershell
python -m pytest -v
```

## 10. Current Limitations and Future Integration

The current backend is developed independently using simulated data.

The following work is planned for the integration phase:

1. Replace simulated resource records with actual cloud collector data.
2. Connect the cost analysis module.
3. Integrate the actual anomaly detection algorithm.
4. Integrate historical-data-based forecasting.
5. Connect the frontend dashboard to the backend endpoints.
6. Validate end-to-end data flow.

The current API structure provides the foundation for these integrations.

## 11. Development Status

The backend API includes:
- FastAPI application initialization
- CORS configuration
- REST endpoint implementation
- Service-layer separation
- Pydantic response validation
- Logging and error handling
- Automated API tests

**Module status:** Independent backend development; actual collector and analyzer integration is pending.
'@ | Set-Content -Path backend\README.md -Encoding UTF8
