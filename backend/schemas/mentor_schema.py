from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class MentorStartRequest(BaseModel):
    student_id: str | None = None
    student_name: str | None = None
    academic_context: dict[str, Any] = Field(default_factory=dict)
    max_questions: int = Field(default=15, ge=8, le=20)


class MentorAnswerRequest(BaseModel):
    answer: str = Field(..., min_length=2, max_length=2500)


class MentorSessionResponse(BaseModel):
    session_id: str
    student_id: str | None = None
    student_name: str | None = None
    academic_context: dict[str, Any]
    status: str
    current_question_number: int
    max_questions: int
    clarity_score: float
    dominant_interest_area: str | None = None
    current_question: str
    current_question_reason: str
    answers: list[dict[str, Any]]


class MentorAnswerResponse(BaseModel):
    session_id: str
    status: str
    current_question_number: int
    max_questions: int
    clarity_score: float
    dominant_interest_area: str | None = None
    previous_answer_analysis: dict[str, Any]
    next_question: str
    why_this_question: str
    ready_for_report: bool
    provider_warning: str | None = None


class MentorReportResponse(BaseModel):
    session_id: str
    student_id: str | None = None
    primary_career_path: str
    secondary_career_paths: list[dict[str, Any]]
    confidence_score: float
    report: dict[str, Any]
    provider_warning: str | None = None
