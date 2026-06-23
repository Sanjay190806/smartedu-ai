from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class AcademicRecord(Base):
    __tablename__ = "academic_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    attendance_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    internal_marks_average: Mapped[float] = mapped_column(Float, nullable=False)
    assignment_completion_rate: Mapped[float] = mapped_column(Float, nullable=False)
    quiz_average: Mapped[float] = mapped_column(Float, nullable=False)
    previous_semester_gpa: Mapped[float] = mapped_column(Float, nullable=False)
    current_gpa: Mapped[float] = mapped_column(Float, nullable=False)
    study_hours_per_week: Mapped[float] = mapped_column(Float, nullable=False)
    backlogs: Mapped[int] = mapped_column(Integer, nullable=False)
    late_submissions: Mapped[int] = mapped_column(Integer, nullable=False)
    participation_score: Mapped[float] = mapped_column(Float, nullable=False)
    subject_math_score: Mapped[float] = mapped_column(Float, nullable=False)
    subject_programming_score: Mapped[float] = mapped_column(Float, nullable=False)
    subject_electronics_score: Mapped[float] = mapped_column(Float, nullable=False)
    subject_communication_score: Mapped[float] = mapped_column(Float, nullable=False)
    subject_lab_score: Mapped[float] = mapped_column(Float, nullable=False)
    library_usage_hours: Mapped[float] = mapped_column(Float, nullable=False)
    lms_login_frequency: Mapped[int] = mapped_column(Integer, nullable=False)
    parent_meeting_count: Mapped[int] = mapped_column(Integer, nullable=False)
    mentor_meeting_count: Mapped[int] = mapped_column(Integer, nullable=False)
    extracurricular_hours: Mapped[float] = mapped_column(Float, nullable=False)
    stress_level: Mapped[int] = mapped_column(Integer, nullable=False)
    sleep_hours: Mapped[float] = mapped_column(Float, nullable=False)
    internet_access: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
