from __future__ import annotations

from pathlib import Path
from typing import Any
import json

import joblib
import numpy as np

from ml.preprocessing import FEATURE_COLUMNS


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_REGISTRY = PROJECT_ROOT / "ml" / "model_registry"


RISK_FEATURE_DIRECTIONS = {
    "attendance_percentage": "low",
    "internal_marks_average": "low",
    "assignment_completion_rate": "low",
    "quiz_average": "low",
    "previous_semester_gpa": "low",
    "current_gpa": "low",
    "study_hours_per_week": "low",
    "backlogs": "high",
    "late_submissions": "high",
    "participation_score": "low",
    "subject_math_score": "low",
    "subject_programming_score": "low",
    "subject_electronics_score": "low",
    "subject_communication_score": "low",
    "subject_lab_score": "low",
    "library_usage_hours": "low",
    "lms_login_frequency": "low",
    "mentor_meeting_count": "low",
    "stress_level": "high",
    "sleep_hours": "low",
}


def get_feature_importance(
    model_path: Path = MODEL_REGISTRY / "model.joblib",
    feature_names_path: Path = MODEL_REGISTRY / "feature_names.json",
) -> list[dict[str, float | str]]:
    model = joblib.load(model_path)
    if feature_names_path.exists():
        feature_names = json.loads(feature_names_path.read_text(encoding="utf-8"))
    else:
        feature_names = FEATURE_COLUMNS

    if hasattr(model, "feature_importances_"):
        values = model.feature_importances_
    elif hasattr(model, "coef_"):
        values = np.mean(np.abs(model.coef_), axis=0)
    else:
        values = np.ones(len(feature_names)) / max(1, len(feature_names))

    pairs = sorted(zip(feature_names, values), key=lambda item: float(item[1]), reverse=True)
    return [{"feature": feature, "importance": float(value)} for feature, value in pairs[:15]]


def explain_prediction(student_data: dict[str, Any], risk_category: str = "Medium Risk") -> dict[str, list[str]]:
    risk_factors: list[str] = []
    protective_factors: list[str] = []

    def add(condition: bool, risk_text: str, protective_text: str | None = None) -> None:
        if condition:
            risk_factors.append(risk_text)
        elif protective_text:
            protective_factors.append(protective_text)

    add(float(student_data.get("attendance_percentage", 100)) < 75, "Attendance is below the expected level.", "Attendance is stable.")
    add(float(student_data.get("assignment_completion_rate", 100)) < 70, "Assignment completion is low.", "Assignment completion is strong.")
    add(float(student_data.get("current_gpa", 10)) < 7, "Current GPA is below the desired range.", "Current GPA is healthy.")
    add(float(student_data.get("previous_semester_gpa", 10)) < 7, "Previous semester GPA was weak.")
    add(float(student_data.get("backlogs", 0)) > 0, "Backlogs are present.", "No active backlog pressure is visible.")
    add(float(student_data.get("study_hours_per_week", 20)) < 10, "Study hours are lower than recommended.")
    add(float(student_data.get("stress_level", 1)) >= 7, "Stress level is high.")
    add(float(student_data.get("sleep_hours", 8)) < 6, "Sleep hours are below a healthy level.")
    add(float(student_data.get("subject_programming_score", 100)) < 60, "Programming score needs focused practice.")
    add(float(student_data.get("subject_math_score", 100)) < 60, "Math score needs revision.")
    add(float(student_data.get("subject_lab_score", 0)) >= 75, "", "Lab score is a protective academic strength.")
    add(float(student_data.get("lms_login_frequency", 0)) >= 12, "", "LMS activity is consistent.")

    risk_factors = [factor for factor in risk_factors if factor]
    protective_factors = [factor for factor in protective_factors if factor]

    return {
        "top_positive_risk_factors": risk_factors[:5],
        "top_protective_factors": protective_factors[:5],
        "risk_category": [risk_category],
    }


def generate_student_friendly_explanation(
    student_data: dict[str, Any],
    risk_category: str,
    factors: list[str] | None = None,
) -> str:
    factors = factors or explain_prediction(student_data, risk_category)["top_positive_risk_factors"]
    if factors:
        joined = "; ".join(factors[:3])
        return (
            f"The model predicts this student as {risk_category} mainly because {joined}. "
            "The strongest improvement areas should be handled with mentor support and a practical weekly plan."
        )
    return (
        f"The model predicts this student as {risk_category}. Current academic signals look mostly stable, "
        "so the focus should be consistency and steady improvement."
    )


def shap_available() -> bool:
    try:
        import shap  # noqa: F401
    except Exception:
        return False
    return True
