from __future__ import annotations

import json

import pandas as pd
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.config import settings
from backend.models.academic_record import AcademicRecord
from backend.models.prediction import Prediction
from backend.models.student import Student


RISK_LABELS = ["Low Risk", "Medium Risk", "High Risk"]
SUBJECT_COLUMNS = {
    "math": "subject_math_score",
    "programming": "subject_programming_score",
    "electronics": "subject_electronics_score",
    "communication": "subject_communication_score",
    "lab": "subject_lab_score",
}


def _empty_risk_counts() -> dict[str, int]:
    return {label: 0 for label in RISK_LABELS}


def _latest_records_subquery(db: Session):
    return (
        db.query(
            AcademicRecord.student_id.label("student_id"),
            func.max(AcademicRecord.id).label("max_id"),
        )
        .group_by(AcademicRecord.student_id)
        .subquery()
    )


def latest_records(db: Session) -> list[AcademicRecord]:
    subq = _latest_records_subquery(db)
    return (
        db.query(AcademicRecord)
        .join(subq, AcademicRecord.id == subq.c.max_id)
        .all()
    )


def risk_distribution(db: Session) -> dict[str, int]:
    counts = _empty_risk_counts()
    rows = db.query(Prediction.risk_category, func.count(Prediction.id)).group_by(Prediction.risk_category).all()
    for label, count in rows:
        counts[label] = int(count)
    return counts


def _summary_from_sample_csv() -> dict:
    path = settings.sample_data_path
    if not path.exists():
        return {
            "total_students": 0,
            "low_risk_count": 0,
            "medium_risk_count": 0,
            "high_risk_count": 0,
            "average_attendance": 0.0,
            "average_gpa": 0.0,
            "average_assignment_completion": 0.0,
            "top_weak_subjects": [],
        }
    df = pd.read_csv(path)
    counts = df.get("risk_label", pd.Series(dtype=str)).value_counts().to_dict()
    subject_means = {
        label: float(df[column].mean())
        for label, column in SUBJECT_COLUMNS.items()
        if column in df.columns
    }
    weak_subjects = sorted(subject_means, key=subject_means.get)[:3]
    return {
        "total_students": int(len(df)),
        "low_risk_count": int(counts.get("Low Risk", 0)),
        "medium_risk_count": int(counts.get("Medium Risk", 0)),
        "high_risk_count": int(counts.get("High Risk", 0)),
        "average_attendance": round(float(df["attendance_percentage"].mean()), 2),
        "average_gpa": round(float(df["current_gpa"].mean()), 2),
        "average_assignment_completion": round(float(df["assignment_completion_rate"].mean()), 2),
        "top_weak_subjects": weak_subjects,
    }


def analytics_summary(db: Session) -> dict:
    total_students = db.query(Student).count()
    records = latest_records(db)
    if total_students == 0 and not records:
        return _summary_from_sample_csv()

    counts = risk_distribution(db)
    subject_means = {
        label: sum(getattr(record, column) for record in records) / len(records)
        for label, column in SUBJECT_COLUMNS.items()
    } if records else {}
    weak_subjects = sorted(subject_means, key=subject_means.get)[:3]
    return {
        "total_students": int(total_students),
        "low_risk_count": counts["Low Risk"],
        "medium_risk_count": counts["Medium Risk"],
        "high_risk_count": counts["High Risk"],
        "average_attendance": round(sum(r.attendance_percentage for r in records) / len(records), 2) if records else 0.0,
        "average_gpa": round(sum(r.current_gpa for r in records) / len(records), 2) if records else 0.0,
        "average_assignment_completion": round(sum(r.assignment_completion_rate for r in records) / len(records), 2) if records else 0.0,
        "top_weak_subjects": weak_subjects,
    }


def department_analytics(db: Session, department: str) -> dict:
    students = db.query(Student).filter(Student.department == department).all()
    ids = [student.student_id for student in students]
    records = db.query(AcademicRecord).filter(AcademicRecord.student_id.in_(ids)).all() if ids else []
    predictions = db.query(Prediction).filter(Prediction.student_id.in_(ids)).all() if ids else []
    counts = _empty_risk_counts()
    for prediction in predictions:
        counts[prediction.risk_category] = counts.get(prediction.risk_category, 0) + 1
    return {
        "department": department,
        "total_students": len(students),
        "risk_distribution": counts,
        "average_gpa": round(sum(r.current_gpa for r in records) / len(records), 2) if records else 0.0,
        "average_attendance": round(sum(r.attendance_percentage for r in records) / len(records), 2) if records else 0.0,
        "high_risk_students": [p.student_id for p in predictions if p.risk_category == "High Risk"],
    }


def subject_performance(db: Session) -> dict[str, float]:
    records = latest_records(db)
    if not records and settings.sample_data_path.exists():
        df = pd.read_csv(settings.sample_data_path)
        return {
            label: round(float(df[column].mean()), 2)
            for label, column in SUBJECT_COLUMNS.items()
        }
    return {
        label: round(sum(getattr(record, column) for record in records) / len(records), 2) if records else 0.0
        for label, column in SUBJECT_COLUMNS.items()
    }
