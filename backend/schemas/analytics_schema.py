from __future__ import annotations

from pydantic import BaseModel


class AnalyticsSummary(BaseModel):
    total_students: int
    low_risk_count: int
    medium_risk_count: int
    high_risk_count: int
    average_attendance: float
    average_gpa: float
    average_assignment_completion: float
    top_weak_subjects: list[str]


class SubjectPerformance(BaseModel):
    math: float
    programming: float
    electronics: float
    communication: float
    lab: float
