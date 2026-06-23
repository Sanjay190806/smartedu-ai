from __future__ import annotations

from pydantic import BaseModel

from backend.schemas.recommendation_schema import RecommendationResponse
from backend.schemas.student_schema import StudentAcademicPayload


class PredictionRequest(StudentAcademicPayload):
    pass


class PredictionResponse(BaseModel):
    student_id: str | None
    risk_category: str
    probability: float
    confidence: str
    top_factors: list[str]
    explanation: str
    recommendations: RecommendationResponse


class BatchPredictionResponse(BaseModel):
    total_records: int
    predictions: list[PredictionResponse]
    risk_distribution: dict[str, int]
