
from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# Common response configuration
class APIResponse(BaseModel):
    pass


# 1. Health API
class HealthResponse(APIResponse):
    status: str
    project: str
    version: str
    timestamp: datetime


# 2. Summary API
class CostBreakdown(BaseModel):
    name: str
    cost: float = Field(ge=0)



class SummaryResponse(APIResponse):
    total_cost: float = Field(ge=0)
    resource_count: int = Field(ge=0)
    average_cost: float = Field(ge=0)
    currency: str = "USD"
    average_utilization: float = Field(ge=0, le=100)
    high_utilization_resources: int = Field(ge=0)
    service_breakdown: List[CostBreakdown]
    region_breakdown: List[CostBreakdown]


# 3. Resources API
class Resource(BaseModel):
    resource_id: str
    resource_type: str
    region: str
    usage: float = Field(ge=0)
    cost: float = Field(ge=0)
    utilization: Optional[float] = Field(default=None, ge=0, le=100)


class ResourcesResponse(APIResponse):
    total_resources: int = Field(ge=0)
    resources: List[Resource]


# 4. Recommendations API
class Recommendation(BaseModel):
    resource_id: str
    recommendation_type: str
    description: str
    estimated_monthly_savings: float = Field(ge=0)
    priority: str


class RecommendationsResponse(APIResponse):
    total_recommendations: int = Field(ge=0)
    recommendations: List[Recommendation]


# 5. Anomalies API
class Anomaly(BaseModel):
    resource_id: str
    date: date
    observed_cost: float = Field(ge=0)
    expected_cost: float = Field(ge=0)
    deviation_percentage: float
    severity: str


class AnomaliesResponse(APIResponse):
    total_anomalies: int = Field(ge=0)
    anomalies: List[Anomaly]


# 6. Forecast API
class ForecastRecord(BaseModel):
    date: date
    predicted_cost: float = Field(ge=0)
    lower_bound: Optional[float] = Field(default=None, ge=0)
    upper_bound: Optional[float] = Field(default=None, ge=0)


class ForecastResponse(APIResponse):
    forecast_period_days: int = Field(default=7, ge=1)
    currency: str = "USD"
    forecast: List[ForecastRecord]
