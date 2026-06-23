from __future__ import annotations

from pathlib import Path
from typing import Any
import sys

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

import joblib

from ml.explainability import explain_prediction, generate_student_friendly_explanation
from ml.preprocessing import coerce_student_record
from ml.recommendation_engine import generate_recommendations


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_REGISTRY = PROJECT_ROOT / "ml" / "model_registry"


def load_artifacts(model_registry: Path = MODEL_REGISTRY):
    model_path = model_registry / "model.joblib"
    preprocessor_path = model_registry / "preprocessor.joblib"
    if not model_path.exists() or not preprocessor_path.exists():
        raise FileNotFoundError("Model artifacts are missing. Run: python ml/train_model.py")
    return joblib.load(model_path), joblib.load(preprocessor_path)


def confidence_from_probability(probability: float) -> str:
    if probability >= 0.80:
        return "High"
    if probability >= 0.60:
        return "Medium"
    return "Low"


def predict_student_risk(student_data: dict[str, Any]) -> dict[str, Any]:
    model, preprocessor = load_artifacts()
    student_frame = coerce_student_record(student_data)
    processed = preprocessor.transform(student_frame)

    predicted_label = str(model.predict(processed)[0])
    probabilities = model.predict_proba(processed)[0]
    class_probabilities = {
        str(label): float(probability)
        for label, probability in zip(model.classes_, probabilities)
    }
    probability = class_probabilities[predicted_label]
    factors = explain_prediction(student_data, predicted_label)
    top_factors = factors["top_positive_risk_factors"]
    explanation = generate_student_friendly_explanation(student_data, predicted_label, top_factors)
    recommendations = generate_recommendations(student_data, predicted_label)

    return {
        "student_id": student_data.get("student_id"),
        "risk_category": predicted_label,
        "probability": round(probability, 4),
        "class_probabilities": class_probabilities,
        "confidence": confidence_from_probability(probability),
        "top_factors": top_factors,
        "protective_factors": factors["top_protective_factors"],
        "explanation": explanation,
        "recommendation_summary": recommendations["summary"],
        "recommendations": recommendations,
    }


def main() -> None:
    sample = {
        "student_id": "DEMO001",
        "department": "Computer Science",
        "year": 3,
        "semester": 5,
        "gender": "Female",
        "attendance_percentage": 62,
        "internal_marks_average": 55,
        "assignment_completion_rate": 58,
        "quiz_average": 52,
        "previous_semester_gpa": 6.1,
        "current_gpa": 5.8,
        "study_hours_per_week": 6,
        "backlogs": 2,
        "late_submissions": 5,
        "participation_score": 45,
        "subject_math_score": 55,
        "subject_programming_score": 49,
        "subject_electronics_score": 60,
        "subject_communication_score": 66,
        "subject_lab_score": 58,
        "library_usage_hours": 2,
        "lms_login_frequency": 4,
        "parent_meeting_count": 1,
        "mentor_meeting_count": 1,
        "extracurricular_hours": 2,
        "stress_level": 8,
        "sleep_hours": 5.2,
        "internet_access": "Yes",
    }
    print(predict_student_risk(sample))


if __name__ == "__main__":
    main()
