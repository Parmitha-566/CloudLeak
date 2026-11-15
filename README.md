# CLOUDLEAK
## Intelligent Cloud Cost Optimization Platform

CLOUDLEAK is a software-based cloud cost monitoring and optimization platform. It analyzes billing data and resource utilization, identifies potentially wasteful resources, detects unusual expenditure patterns, generates optimization recommendations, and forecasts future costs.

The project integrates a Python analysis engine, FastAPI backend, Streamlit dashboard, Docker containers, and Kubernetes deployment resources.

## 1. Project Objectives

- Monitor cloud resource expenditure.
- Analyze resource utilization and identify underutilized resources.
- Detect unusual historical cost patterns.
- Generate cost optimization recommendations.
- Forecast expenditure for the next seven days.
- Present results through an interactive dashboard.
- Demonstrate containerization and orchestration using Docker and Kubernetes.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas and NumPy | Data processing and numerical analysis |
| FastAPI | REST API backend |
| Pydantic | API response validation |
| Streamlit | Interactive dashboard |
| Plotly | Interactive charts |
| Pytest | Automated testing |
| Docker | Application containerization |
| Docker Compose | Multi-container application execution |
| Kubernetes | Application orchestration |
| Minikube | Local Kubernetes environment |
| GitHub Actions | Continuous integration |

## 3. System Architecture

```text
             Billing and Historical Data
                         |
                         v
                Member 1 Data Loader
                         |
                         v
                 Analyzer Modules
          +--------------+--------------+
          |              |              |
          v              v              v
      Cost Analysis  Anomaly Detection  Forecasting
          |              |              |
          +--------------+--------------+
                         |
                         v
                  FastAPI Backend
                         |
                 REST API Endpoints
                         |
                         v
                 Streamlit Dashboard
                         |
                         v
             Charts, Metrics and Reports
```

Docker packages the backend and dashboard into separate containers. Docker Compose runs both services together, while Kubernetes manifests support deployment and management in a local cluster.

## 4. Project Structure

```text
CloudLeak/
|
+-- analyzer/
|   +-- anomaly_detection.py
|   +-- cost_analysis.py
|   +-- forecasting.py
|   +-- recommendations.py
|
+-- backend/
|   +-- main.py
|   +-- README.md
|   +-- schemas/
|   |   +-- response_models.py
|   +-- services/
|   |   +-- analysis_service.py
|   |   +-- data_service.py
|   +-- utils/
|
+-- dashboard/
|   +-- app.py
|   +-- api_client.py
|
+-- Member1/
|   +-- sample_billing.csv
|   +-- historical_costs.csv
|   +-- cloud_resource_module.py
|   +-- generate_historical.py
|   +-- collector/
|       +-- data_loader.py
|
+-- tests/
|   +-- test_analysis_service.py
|   +-- test_analyzer.py
|   +-- test_api.py
|   +-- test_dashboard_data.py
|   +-- test_data_service.py
|
+-- k8s/
|   +-- configmap.yaml
|   +-- deployment.yaml
|   +-- service.yaml
|   +-- hpa.yaml
|   +-- dashboard-deployment.yaml
|   +-- dashboard-service.yaml
|   +-- kustomization.yaml
|
+-- .github/
|   +-- workflows/
|       +-- ci.yml
|
+-- Dockerfile
+-- Dockerfile.dashboard
+-- compose.yaml
+-- requirements.txt
+-- README.md
```

## 5. Main Features

### Cost Analysis

- Calculates total expenditure and average resource cost.
- Groups expenditure by resource type and region.
- Analyzes CPU and memory utilization.
- Identifies underutilized resources.

### Optimization Recommendations

The current recommendation engine uses these utilization rules:

- At or below 5% utilization: investigate stopping the resource.
- Above 5% and below 20%: consider downsizing.
- At or above 20%: no underutilization recommendation.

Estimated savings are based on assumptions and should not be interpreted as guaranteed savings.

### Anomaly Detection

The anomaly detection module evaluates historical daily expenditure using a median and median absolute deviation (MAD) baseline.

It compares observations against the previous seven available observations for the same identifier, with fallback thresholds.

The current historical dataset is grouped by cloud provider, so anomaly identifiers represent providers rather than individual cloud resources.

### Cost Forecasting

The forecasting module uses the most recent seven daily expenditure observations to calculate an average daily cost.

It uses this average to forecast expenditure for the next seven calendar days.

Current implementation limitations:

- The forecast horizon is fixed at seven days.
- The method is a moving-average baseline, not a trained machine-learning model.
- Confidence intervals are not calculated.
- Lower and upper forecast bounds are returned as null.
- At least seven historical observations are required.

## 6. Interactive Dashboard

The Streamlit dashboard provides:

- Total monthly expenditure.
- Total cloud resource count.
- Average resource utilization.
- Flagged resource metrics.
- Expenditure breakdown by resource type.
- Resource utilization visualization.
- Regional expenditure analysis.
- Seven-day cost forecasting.
- Resource and region filters.
- USD and INR currency selection.
- What-If Policy Simulator.

The dashboard communicates with the FastAPI backend through the API client.

## 7. Backend API

The FastAPI application exposes the following endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/health` | Backend health check |
| GET | `/api/summary` | Overall cost and resource metrics |
| GET | `/api/resources` | Resource information |
| GET | `/api/recommendations` | Optimization recommendations |
| GET | `/api/anomalies` | Detected cost anomalies |
| GET | `/api/forecast` | Seven-day expenditure forecast |

Interactive API documentation:

`http://localhost:8006/docs` when running through Docker Compose.

## 8. Data Sources

The project uses demonstration billing and historical cost datasets:

- `Member1/sample_billing.csv`
- `Member1/historical_costs.csv`

The data loader validates the input data before it is passed to the analysis modules.

The project is designed to demonstrate cloud cost analysis without requiring paid cloud infrastructure.

## 9. Installation and Local Execution

### Prerequisites

- Python 3.10 or later
- Git
- Visual Studio Code (recommended)

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

### Run the backend

From the project root, open a terminal and run:

```powershell
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Backend API:

`http://127.0.0.1:8000`

Swagger documentation:

`http://127.0.0.1:8000/docs`

### Run the dashboard

Open a second terminal, activate the virtual environment, and run:

```powershell
python -m streamlit run dashboard/app.py
```

The dashboard normally opens at:

`http://localhost:8501`

For local execution, ensure the dashboard API URL is configured to reach the locally running backend.

## 10. Docker and Docker Compose

The project provides separate Dockerfiles for the backend and dashboard.

Build and start both services from the project root:

```powershell
docker compose up -d --build
```

Check running services:

```powershell
docker compose ps
```

Access the application:

| Component | URL |
|---|---|
| Dashboard | http://localhost:8502 |
| Backend API | http://localhost:8006 |
| Swagger documentation | http://localhost:8006/docs |

View service logs:

```powershell
docker compose logs
```

The Compose configuration connects the dashboard to the backend using the internal service address.

## 11. Kubernetes Deployment

The `k8s/` directory contains Kubernetes resources for the backend and dashboard.

The configuration includes:

- Backend Deployment and Service.
- Dashboard Deployment and Service.
- ConfigMap.
- Horizontal Pod Autoscaler.
- Kustomize resource configuration.
- Container health probes and resource settings.

Build the local images:

```powershell
docker build -t cloudleak-backend:1.0 -f Dockerfile .
docker build -t cloudleak-dashboard:1.0 -f Dockerfile.dashboard .
```

Load the images into Minikube:

```powershell
minikube image load cloudleak-backend:1.0
minikube image load cloudleak-dashboard:1.0
```

Apply the Kubernetes resources:

```powershell
kubectl apply -k .\k8s
```

Check deployment status:

```powershell
kubectl get all -n cloudleak
```

Check autoscaling configuration:

```powershell
kubectl get hpa -n cloudleak
```

Access the dashboard using port forwarding:

```powershell
kubectl port-forward -n cloudleak svc/cloudleak-dashboard 8503:8501
```

Open:

`http://localhost:8503`

## 12. Automated Testing

Run the complete test suite from the project root:

```powershell
python -m pytest -q
```

Run tests with detailed output:

```powershell
python -m pytest -v
```

Check Python syntax:

```powershell
python -m compileall backend analyzer dashboard Member1 tests
```

The project includes tests for data processing, analysis modules, API endpoints, dashboard data handling, recommendations, anomaly detection, and forecasting.

## 13. Continuous Integration

GitHub Actions is configured through:

`.github/workflows/ci.yml`

The CI workflow:

1. Checks out the repository.
2. Sets up Python.
3. Installs project dependencies.
4. Runs the automated test suite.
5. Builds the backend Docker image.
6. Builds the dashboard Docker image.

The workflow runs on pushes and pull requests.

## 14. Current Implementation Status

Implemented and tested:

- Billing and historical data integration.
- Cost and resource utilization analysis.
- Optimization recommendation engine.
- Historical cost anomaly detection.
- Seven-day cost forecasting.
- FastAPI backend with six REST endpoints.
- Streamlit dashboard and API integration.
- Dashboard filters, currency selection, and visualizations.
- Docker images and Docker Compose configuration.
- Kubernetes backend and dashboard deployments.
- Kubernetes service connectivity and dashboard access.
- Dashboard pod recovery through Kubernetes Deployment.
- Automated Python tests.
- GitHub Actions test and Docker build workflow.

## 15. Known Limitations and Future Improvements

Current limitations:

- Input data is demonstration billing data rather than live cloud-provider billing.
- Forecasting uses a moving-average baseline.
- Forecast confidence intervals are not implemented.
- Anomaly detection operates on the available historical observations.
- Estimated savings are assumptions, not guaranteed outcomes.

Potential future improvements:

- Integrate live AWS, Azure, or Google Cloud billing APIs.
- Add machine-learning-based cost forecasting.
- Improve anomaly detection with additional historical features.
- Add configurable optimization policies.
- Add user authentication and role-based access control.
- Support downloadable cost and optimization reports.

---

## Project Information

**Project:** CLOUDLEAK
**Title:** Intelligent Cloud Cost Optimization Platform
**Backend:** FastAPI and Python
**Dashboard:** Streamlit
**Containerization:** Docker and Docker Compose
**Orchestration:** Kubernetes and Minikube
**Continuous Integration:** GitHub Actions
**Repository:** https://github.com/Parmitha-566/CloudLeak
