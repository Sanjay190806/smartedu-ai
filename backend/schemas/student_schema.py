from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class StudentBase(BaseModel):
    student_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    department: str = Field(..., min_length=1)
    year: int = Field(..., ge=1, le=4)
    semester: int = Field(..., ge=1, le=8)
    gender: str = Field(..., min_length=1)


class AcademicRecordBase(BaseModel):
    attendance_percentage: float = Field(..., ge=0, le=100)
    internal_marks_average: float = Field(..., ge=0, le=100)
    assignment_completion_rate: float = Field(..., ge=0, le=100)
    quiz_average: float = Field(..., ge=0, le=100)
    previous_semester_gpa: float = Field(..., ge=0, le=10)
    current_gpa: float = Field(..., ge=0, le=10)
    study_hours_per_week: float = Field(..., ge=0, le=80)
    backlogs: int = Field(..., ge=0)
    late_submissions: int = Field(..., ge=0)
    participation_score: float = Field(..., ge=0, le=100)
    subject_math_score: float = Field(..., ge=0, le=100)
    subject_programming_score: float = Field(..., ge=0, le=100)
    subject_electronics_score: float = Field(..., ge=0, le=100)
    subject_communication_score: float = Field(..., ge=0, le=100)
    subject_lab_score: float = Field(..., ge=0, le=100)
    library_usage_hours: float = Field(..., ge=0)
    lms_login_frequency: int = Field(..., ge=0)
    parent_meeting_count: int = Field(..., ge=0)
    mentor_meeting_count: int = Field(..., ge=0)
    extracurricular_hours: float = Field(..., ge=0)
    stress_level: int = Field(..., ge=1, le=10)
    sleep_hours: float = Field(..., ge=0, le=12)
    internet_access: str = Field(..., min_length=1)


class StudentAcademicPayload(StudentBase, AcademicRecordBase):
    pass


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    department: str | None = Field(default=None, min_length=1)
    year: int | None = Field(default=None, ge=1, le=4)
    semester: int | None = Field(default=None, ge=1, le=8)
    gender: str | None = Field(default=None, min_length=1)
    attendance_percentage: float | None = Field(default=None, ge=0, le=100)
    internal_marks_average: float | None = Field(default=None, ge=0, le=100)
    assignment_completion_rate: float | None = Field(default=None, ge=0, le=100)
    quiz_average: float | None = Field(default=None, ge=0, le=100)
    previous_semester_gpa: float | None = Field(default=None, ge=0, le=10)
    current_gpa: float | None = Field(default=None, ge=0, le=10)
    study_hours_per_week: float | None = Field(default=None, ge=0, le=80)
    backlogs: int | None = Field(default=None, ge=0)
    late_submissions: int | None = Field(default=None, ge=0)
    participation_score: float | None = Field(default=None, ge=0, le=100)
    subject_math_score: float | None = Field(default=None, ge=0, le=100)
    subject_programming_score: float | None = Field(default=None, ge=0, le=100)
    subject_electronics_score: float | None = Field(default=None, ge=0, le=100)
    subject_communication_score: float | None = Field(default=None, ge=0, le=100)
    subject_lab_score: float | None = Field(default=None, ge=0, le=100)
    library_usage_hours: float | None = Field(default=None, ge=0)
    lms_login_frequency: int | None = Field(default=None, ge=0)
    parent_meeting_count: int | None = Field(default=None, ge=0)
    mentor_meeting_count: int | None = Field(default=None, ge=0)
    extracurricular_hours: float | None = Field(default=None, ge=0)
    stress_level: int | None = Field(default=None, ge=1, le=10)
    sleep_hours: float | None = Field(default=None, ge=0, le=12)
    internet_access: str | None = Field(default=None, min_length=1)


class AcademicRecordResponse(AcademicRecordBase):
    id: int
    student_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StudentResponse(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    latest_academic_record: AcademicRecordResponse | None = None

    model_config = ConfigDict(from_attributes=True)
