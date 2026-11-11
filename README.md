# CLOUDLEAK — Backend API

## 1. Project Overview

CLOUDLEAK is an Intelligent Cloud Cost Optimization Platform designed to analyze cloud resource expenditure, identify anomalies, generate cost optimization recommendations, and forecast future expenditure.

This repository contains the backend API developed using **FastAPI and Python**.

The backend exposes REST API endpoints that can be consumed by the frontend application.

## 2. Member 3 Responsibilities

Member 3 — Backend and API Engineer:

- Develop the FastAPI application.
- Implement REST API endpoints.
- Create Pydantic response models.
- Implement data and analysis service interfaces.
- Configure CORS for frontend communication.
- Implement error handling and logging.
- Develop automated API and service tests.
- Prepare API documentation.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| Pydantic | Response validation |
| Pandas | Data processing dependency |
| NumPy | Numerical processing dependency |
| Pytest | Automated testing |
| HTTPX | API testing client |

## 4. Project Structure

```text
CloudLeak/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── response_models.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── data_service.py
│   │   └── analysis_service.py
│   │
│   └── utils/
│       └── __init__.py
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_data_service.py
│   └── test_analysis_service.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## 5. Installation and Setup

### Prerequisites

- Python 3.10 or later
- Git
- Visual Studio Code

### Clone the repository

```powershell
git clone https://github.com/Parmitha-566/CloudLeak.git
cd CloudLeak
```

### Create a virtual environment

```powershell
python -m venv .venv
```

### Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## 6. Running the Backend

Start the FastAPI application using:

```powershell
python -m uvicorn backend.main:app --reload
```

The backend runs at:

`http://127.0.0.1:8000`

Interactive Swagger documentation:

`http://127.0.0.1:8000/docs`

OpenAPI specification:

`http://127.0.0.1:8000/openapi.json`

## 7. API Endpoints

All endpoints use the HTTP GET method.

| Endpoint | Description |
|---|---|
| `/api/health` | Checks backend health |
| `/api/summary` | Returns expenditure and utilization summary |
| `/api/resources` | Returns cloud resource information |
| `/api/recommendations` | Returns optimization recommendations |
| `/api/anomalies` | Returns detected cost anomalies |
| `/api/forecast` | Returns a seven-day expenditure forecast |

### Health Check

`GET /api/health`

Returns backend status, project name, version and timestamp.

### Cost Summary

`GET /api/summary`

Returns:

- Total expenditure
- Resource count
- Average resource cost
- Average utilization
- High-utilization resource count
- Cost breakdown by service
- Cost breakdown by region

### Resources

`GET /api/resources`

Returns cloud resource identifiers, resource types, regions, usage, cost and utilization.

### Recommendations

`GET /api/recommendations`

Returns resource optimization recommendations, estimated monthly savings and priority.

### Anomalies

`GET /api/anomalies`

Returns detected cost anomalies, observed expenditure, expected expenditure, deviation percentage and severity.

### Forecast

`GET /api/forecast`

Returns predicted expenditure for the next seven days, including lower and upper estimate bounds.

## 8. Example API Responses

The following examples illustrate the current demonstration-data response format. Timestamps and forecast dates vary.

### Health

```json
{
  "status": "healthy",
  "project": "CLOUDLEAK",
  "version": "1.0.0",
  "timestamp": "2026-11-11T12:00:00+00:00"
}
```

### Summary

```json
{
  "total_cost": 903.5,
  "resource_count": 5,
  "average_cost": 180.7,
  "currency": "USD",
  "average_utilization": 60.4,
  "high_utilization_resources": 1,
  "service_breakdown": [
    {"name": "EC2", "cost": 675.5},
    {"name": "RDS", "cost": 185.75},
    {"name": "S3", "cost": 42.25}
   ],
   "region_breakdown": [
    {"name": "ap-south-1", "cost": 362.25},
    {"name": "us-east-1", "cost": 331.25},
    {"name": "us-west-2", "cost": 210.0}
   ]
}
```

### Resources

```json
{
  "total_resources": 5,
  "resources": [
    {
      "resource_id": "EC2-001",
      "resource_type": "EC2",
      "region": "us-east-1",
      "usage": 720.0,
      "cost": 145.5,
      "utilization": 28.0
    }
  ]
}
```

### Recommendations

```json
{
  "total_recommendations": 3,
  "recommendations": []
}
```

### Anomalies

```json
{
  "total_anomalies": 2,
  "anomalies": []
}
```

### Forecast

```json
{
  "forecast_period_days": 7,
  "currency": "USD",
  "forecast": [
    {
      "date": "2026-11-12",
      "predicted_cost": 30.42,
      "lower_bound": 27.38,
      "upper_bound": 33.46
    }
  ]
}
```

The empty arrays and single-item arrays above are abbreviated examples; actual endpoints return their available records.

## 9. CORS Configuration

The backend permits frontend requests from:

- `http://localhost:8501`
- `http://127.0.0.1:8501`

These origins support local Streamlit frontend development.

## 10. Error Handling

The backend uses HTTP status codes to communicate errors.

| Status code | Meaning |
|---|---|
| 200 | Successful request |
| 400 | Invalid request or forecast input |
| 500 | Internal server error |

Internal failures are recorded using Python logging. Internal exception details should not be exposed in generic server-error responses.

## 11. Automated Testing

Run the test suite:

```powershell
python -m pytest -v
```

Check Python syntax:

```powershell
python -m compileall backend tests
```

The tests cover:

- API endpoint responses
- Data service calculations
- Recommendation generation
- Anomaly detection
- Forecast generation
- Error handling
- CORS preflight behavior
- API documentation availability

## 12. Current Development Status

The backend currently uses temporary simulated cloud resource data and demonstration analysis logic.

The forecast is a mathematical demonstration projection, not a trained machine-learning model.

Integration with the actual collector and analyzer modules is pending until the respective team members provide their implementations and agreed interfaces.

The temporary services are intended for independent backend development and API testing.

## 13. Future Integration

The backend will be connected to:

- Member 1's cloud data loader.
- Member 2's analysis and optimization functions.

The service layer and response schemas will be adapted to the actual integrated data structures and function interfaces.

---

**CLOUDLEAK — Intelligent Cloud Cost Optimization Platform**

**Module:** Backend and API Engineering  
**Framework:** FastAPI  
**Language:** Python