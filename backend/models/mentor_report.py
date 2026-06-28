from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class MentorReport(Base):
    __tablename__ = "mentor_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    student_id: Mapped[str | None] = mapped_column(String, nullable=True, index=True)
    report_json: Mapped[str] = mapped_column(Text, nullable=False)
    primary_career_path: Mapped[str] = mapped_column(String, nullable=False)
    secondary_career_paths_json: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
