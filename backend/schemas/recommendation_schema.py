from __future__ import annotations

from pydantic import BaseModel

from backend.schemas.student_schema import StudentAcademicPayload


class RecommendationGenerateRequest(StudentAcademicPayload):
    risk_category: str = "Medium Risk"


class RecommendationResponse(BaseModel):
    student_id: str | None = None
    risk_category: str
    summary: str
    top_problems: list[str]
    action_plan: list[str]
    seven_day_plan: list[str]
    thirty_day_plan: list[str]
    resources: list[str] = []
    mentor_note: str
