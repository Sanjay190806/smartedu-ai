from __future__ import annotations

from typing import Any

from ml.recommendation_engine import generate_recommendations


def normalize_recommendation(
    student_data: dict[str, Any],
    risk_category: str,
) -> dict[str, Any]:
    raw = generate_recommendations(student_data, risk_category)
    return {
        "student_id": raw.get("student_id") or student_data.get("student_id"),
        "risk_category": raw.get("risk_category") or risk_category,
        "summary": raw.get("summary", ""),
        "top_problems": raw.get("top_problems") or raw.get("top_3_problems", []),
        "action_plan": raw.get("action_plan") or raw.get("top_5_actions", []),
        "seven_day_plan": raw.get("seven_day_plan", []),
        "thirty_day_plan": raw.get("thirty_day_plan", []),
        "resources": raw.get("resources", []),
        "mentor_note": raw.get("mentor_note", ""),
    }
