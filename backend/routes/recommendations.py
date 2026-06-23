from __future__ import annotations

import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.recommendation import Recommendation
from backend.schemas.recommendation_schema import RecommendationGenerateRequest, RecommendationResponse
from backend.services.recommendation_service import normalize_recommendation


router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


def recommendation_model_to_dict(recommendation: Recommendation) -> dict:
    return {
        "student_id": recommendation.student_id,
        "risk_category": recommendation.risk_category,
        "summary": recommendation.summary,
        "top_problems": json.loads(recommendation.top_problems_json),
        "action_plan": json.loads(recommendation.action_plan_json),
        "seven_day_plan": json.loads(recommendation.seven_day_plan_json),
        "thirty_day_plan": json.loads(recommendation.thirty_day_plan_json),
        "resources": json.loads(getattr(recommendation, "resources_json", "[]") or "[]"),
        "mentor_note": recommendation.mentor_note,
    }


@router.get("/{student_id}", response_model=RecommendationResponse)
def get_recommendation(student_id: str, db: Session = Depends(get_db)):
    recommendation = (
        db.query(Recommendation)
        .filter(Recommendation.student_id == student_id)
        .order_by(Recommendation.created_at.desc(), Recommendation.id.desc())
        .first()
    )
    if recommendation is None:
        raise HTTPException(status_code=404, detail="Recommendation not found for this student")
    return recommendation_model_to_dict(recommendation)


@router.post("/generate", response_model=RecommendationResponse)
def generate_recommendation(payload: RecommendationGenerateRequest):
    data = payload.model_dump()
    risk_category = data.pop("risk_category")
    return normalize_recommendation(data, risk_category)
