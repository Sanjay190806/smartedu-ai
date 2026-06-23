from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any
import json

import joblib
from sqlalchemy.orm import Session

from backend.config import settings
from backend.models.prediction import Prediction
from backend.models.recommendation import Recommendation
from backend.schemas.student_schema import StudentAcademicPayload
from backend.services.recommendation_service import normalize_recommendation
from backend.services.student_service import create_or_update_student_with_record
from ml.explainability import explain_prediction, generate_student_friendly_explanation
from ml.preprocessing import coerce_student_record


class ModelArtifactError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def load_model_artifacts() -> tuple[Any, Any]:
    model_path = Path(settings.model_path)
    preprocessor_path = Path(settings.preprocessor_path)
    if not model_path.exists() or not preprocessor_path.exists():
        raise ModelArtifactError("Model artifacts not found. Run python ml/train_model.py first.")
    return joblib.load(model_path), joblib.load(preprocessor_path)


def model_is_available() -> bool:
    try:
        load_model_artifacts()
    except Exception:
        return False
    return True


def confidence_from_probability(probability: float) -> str:
    if probability >= 0.80:
        return "High"
    if probability >= 0.60:
        return "Medium"
    return "Low"


def predict_payload(payload: StudentAcademicPayload) -> dict[str, Any]:
    model, preprocessor = load_model_artifacts()
    student_data = payload.model_dump()
    student_frame = coerce_student_record(student_data)
    processed = preprocessor.transform(student_frame)
    risk_category = str(model.predict(processed)[0])
    probabilities = model.predict_proba(processed)[0]
    class_probabilities = {
        str(label): float(probability)
        for label, probability in zip(model.classes_, probabilities)
    }
    probability = class_probabilities[risk_category]
    factors = explain_prediction(student_data, risk_category)
    top_factors = factors.get("top_positive_risk_factors", [])
    explanation = generate_student_friendly_explanation(student_data, risk_category, top_factors)
    recommendation = normalize_recommendation(student_data, risk_category)
    return {
        "student_id": payload.student_id,
        "risk_category": risk_category,
        "probability": round(float(probability), 4),
        "confidence": confidence_from_probability(float(probability)),
        "top_factors": top_factors,
        "explanation": explanation,
        "recommendations": recommendation,
    }


def predict_and_persist(db: Session, payload: StudentAcademicPayload) -> dict[str, Any]:
    create_or_update_student_with_record(db, payload)
    result = predict_payload(payload)
    recommendation = result["recommendations"]
    db.add(
        Prediction(
            student_id=payload.student_id,
            risk_category=result["risk_category"],
            probability=result["probability"],
            confidence=result["confidence"],
            top_factors_json=json.dumps(result["top_factors"]),
            explanation=result["explanation"],
        )
    )
    saved_recommendation = Recommendation(
        student_id=payload.student_id,
        risk_category=result["risk_category"],
        summary=recommendation["summary"],
        top_problems_json=json.dumps(recommendation["top_problems"]),
        action_plan_json=json.dumps(recommendation["action_plan"]),
        seven_day_plan_json=json.dumps(recommendation["seven_day_plan"]),
        thirty_day_plan_json=json.dumps(recommendation["thirty_day_plan"]),
        resources_json=json.dumps(recommendation.get("resources", [])),
        mentor_note=recommendation["mentor_note"],
    )
    db.add(saved_recommendation)
    db.flush()
    if saved_recommendation.id is None:
        raise RuntimeError("Generated recommendation was not persisted.")
    db.commit()
    db.refresh(saved_recommendation)
    return result
