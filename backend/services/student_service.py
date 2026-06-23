from __future__ import annotations

from sqlalchemy.orm import Session

from backend.models.academic_record import AcademicRecord
from backend.models.prediction import Prediction
from backend.models.recommendation import Recommendation
from backend.models.student import Student
from backend.schemas.student_schema import StudentAcademicPayload, StudentUpdate


PROFILE_FIELDS = ["student_id", "name", "department", "year", "semester", "gender"]
ACADEMIC_FIELDS = [
    "attendance_percentage", "internal_marks_average", "assignment_completion_rate",
    "quiz_average", "previous_semester_gpa", "current_gpa", "study_hours_per_week",
    "backlogs", "late_submissions", "participation_score", "subject_math_score",
    "subject_programming_score", "subject_electronics_score", "subject_communication_score",
    "subject_lab_score", "library_usage_hours", "lms_login_frequency",
    "parent_meeting_count", "mentor_meeting_count", "extracurricular_hours",
    "stress_level", "sleep_hours", "internet_access",
]


def latest_academic_record(db: Session, student_id: str) -> AcademicRecord | None:
    return (
        db.query(AcademicRecord)
        .filter(AcademicRecord.student_id == student_id)
        .order_by(AcademicRecord.created_at.desc(), AcademicRecord.id.desc())
        .first()
    )


def student_to_response(db: Session, student: Student) -> dict:
    data = {
        "id": student.id,
        "student_id": student.student_id,
        "name": student.name,
        "department": student.department,
        "year": student.year,
        "semester": student.semester,
        "gender": student.gender,
        "created_at": student.created_at,
        "updated_at": student.updated_at,
        "latest_academic_record": latest_academic_record(db, student.student_id),
    }
    return data


def get_student(db: Session, student_id: str) -> Student | None:
    return db.query(Student).filter(Student.student_id == student_id).first()


def create_or_update_student_with_record(
    db: Session,
    payload: StudentAcademicPayload,
) -> Student:
    data = payload.model_dump()
    student = get_student(db, payload.student_id)
    if student is None:
        student = Student(**{field: data[field] for field in PROFILE_FIELDS})
        db.add(student)
    else:
        for field in PROFILE_FIELDS:
            if field != "student_id":
                setattr(student, field, data[field])

    record = AcademicRecord(
        student_id=payload.student_id,
        **{field: data[field] for field in ACADEMIC_FIELDS},
    )
    db.add(record)
    db.commit()
    db.refresh(student)
    return student


def update_student(db: Session, student: Student, payload: StudentUpdate) -> Student:
    update_data = payload.model_dump(exclude_unset=True)
    for field in ["name", "department", "year", "semester", "gender"]:
        if field in update_data:
            setattr(student, field, update_data[field])

    if any(field in update_data for field in ACADEMIC_FIELDS):
        latest = latest_academic_record(db, student.student_id)
        base = {field: getattr(latest, field) for field in ACADEMIC_FIELDS} if latest else {}
        base.update({field: update_data[field] for field in ACADEMIC_FIELDS if field in update_data})
        missing = sorted(set(ACADEMIC_FIELDS) - set(base))
        if missing:
            raise ValueError(f"Cannot create partial academic record without existing values: {missing}")
        db.add(AcademicRecord(student_id=student.student_id, **base))

    db.commit()
    db.refresh(student)
    return student


def delete_student_and_related(db: Session, student: Student) -> None:
    student_id = student.student_id
    db.query(AcademicRecord).filter(AcademicRecord.student_id == student_id).delete()
    db.query(Prediction).filter(Prediction.student_id == student_id).delete()
    db.query(Recommendation).filter(Recommendation.student_id == student_id).delete()
    db.delete(student)
    db.commit()
