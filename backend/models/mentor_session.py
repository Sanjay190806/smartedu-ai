from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class MentorSession(Base):
    __tablename__ = "mentor_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    student_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    student_name: Mapped[str | None] = mapped_column(String, nullable=True)
    academic_context_json: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    status: Mapped[str] = mapped_column(String, default="active", nullable=False)
    current_question_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    max_questions: Mapped[int] = mapped_column(Integer, default=15, nullable=False)
    clarity_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    dominant_interest_area: Mapped[str | None] = mapped_column(String, nullable=True)
    current_question_text: Mapped[str] = mapped_column(Text, nullable=False)
    current_question_reason: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
