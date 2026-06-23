from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    risk_category: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    top_problems_json: Mapped[str] = mapped_column(Text, nullable=False)
    action_plan_json: Mapped[str] = mapped_column(Text, nullable=False)
    seven_day_plan_json: Mapped[str] = mapped_column(Text, nullable=False)
    thirty_day_plan_json: Mapped[str] = mapped_column(Text, nullable=False)
    resources_json: Mapped[str] = mapped_column(Text, default="[]", nullable=False)
    mentor_note: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
