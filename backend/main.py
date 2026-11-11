import logging
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.services import data_service, analysis_service

from backend.schemas.response_models import (
    HealthResponse,
    SummaryResponse,
    ResourcesResponse,
    RecommendationsResponse,
    AnomaliesResponse,
    ForecastResponse
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("CLOUDLEAK")

# --------------------------------------------------
# FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="CLOUDLEAK API",
    description=(
        "Backend API for the Intelligent Cloud Cost "
        "Optimization Platform"
    ),
    version="1.0.0"
)


# --------------------------------------------------
# CORS CONFIGURATION
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# --------------------------------------------------
# ROOT ENDPOINT
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Welcome to CLOUDLEAK API",
        "documentation": "/docs"
    }


# --------------------------------------------------
# 1. HEALTH ENDPOINT
# --------------------------------------------------

@app.get("/api/health", response_model=HealthResponse)
def health_check():

    return {
        "status": "healthy",
        "project": "CLOUDLEAK",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc)
    }


# --------------------------------------------------
# 2. SUMMARY ENDPOINT
# --------------------------------------------------

@app.get("/api/summary", response_model=SummaryResponse)
def get_summary():

    try:
        resources = data_service.get_resources()

        if not resources:
            average_utilization = 0.0
            high_utilization = 0
        else:
            utilization_values = [
                resource["utilization"]
                for resource in resources
                if resource.get("utilization") is not None
            ]

            average_utilization = (
                sum(utilization_values) / len(utilization_values)
                if utilization_values else 0.0
            )

            high_utilization = sum(
                value > 85 for value in utilization_values
            )

        return {
            "total_cost": data_service.get_total_cost(),
            "resource_count": data_service.get_resource_count(),
            "average_cost": data_service.get_average_cost(),
            "currency": "USD",
            "average_utilization": round(average_utilization, 2),
            "high_utilization_resources": high_utilization,
            "service_breakdown": data_service.get_cost_breakdown(
                "resource_type"
            ),
            "region_breakdown": data_service.get_cost_breakdown(
                "region"
            )
        }

    except Exception:
        logger.exception("Failed to generate summary")

        raise HTTPException(
            status_code=500,
            detail="Internal server error while generating summary."
        )

# --------------------------------------------------
# 3. RESOURCES ENDPOINT
# --------------------------------------------------


@app.get("/api/resources", response_model=ResourcesResponse)
def get_resources():
    try:
        resources = data_service.get_resources()

        return {
            "total_resources": len(resources),
            "resources": resources
        }

    except Exception:
        logger.exception("Failed to retrieve resources")

        raise HTTPException(
            status_code=500,
            detail="Internal server error while retrieving resources."
        )


# --------------------------------------------------
# 4. RECOMMENDATIONS ENDPOINT
# --------------------------------------------------


@app.get(
    "/api/recommendations",
    response_model=RecommendationsResponse
)
def get_recommendations():
    try:
        recommendations = (
            analysis_service.generate_recommendations()
        )

        return {
            "total_recommendations": len(recommendations),
            "recommendations": recommendations
        }

    except Exception:
        logger.exception("Failed to generate recommendations")

        raise HTTPException(
            status_code=500,
            detail="Internal server error while generating recommendations."
        )



# --------------------------------------------------
# 5. ANOMALIES ENDPOINT
# --------------------------------------------------


@app.get("/api/anomalies", response_model=AnomaliesResponse)
def get_anomalies():
    try:
        anomalies = analysis_service.detect_anomalies()

        return {
            "total_anomalies": len(anomalies),
            "anomalies": anomalies
        }

    except Exception:
        logger.exception("Failed to detect anomalies")

        raise HTTPException(
            status_code=500,
            detail="Internal server error while detecting anomalies."
        )



# --------------------------------------------------
# 6. FORECAST ENDPOINT
# --------------------------------------------------


@app.get("/api/forecast", response_model=ForecastResponse)
def get_forecast():
    try:
        forecast = analysis_service.generate_forecast(days=7)

        return {
            "forecast_period_days": 7,
            "currency": "USD",
            "forecast": forecast
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    except Exception:
        logger.exception("Failed to generate forecast")

        raise HTTPException(
            status_code=500,
            detail="Internal server error while generating forecast."
        )
