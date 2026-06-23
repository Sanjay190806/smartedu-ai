from __future__ import annotations

from typing import Any

import pandas as pd

from dashboard.config import REQUIRED_STUDENT_COLUMNS


def get_missing_columns(df: pd.DataFrame) -> list[str]:
    return sorted(set(REQUIRED_STUDENT_COLUMNS) - set(df.columns))


def validate_csv_columns(df: pd.DataFrame) -> tuple[bool, list[str]]:
    missing = get_missing_columns(df)
    return len(missing) == 0, missing


def validate_student_payload(payload: dict[str, Any]) -> tuple[bool, list[str]]:
    errors: list[str] = []
    missing = [column for column in REQUIRED_STUDENT_COLUMNS if column not in payload]
    if missing:
        errors.append(f"Missing fields: {', '.join(missing)}")

    ranges = {
        "attendance_percentage": (0, 100),
        "internal_marks_average": (0, 100),
        "assignment_completion_rate": (0, 100),
        "quiz_average": (0, 100),
        "previous_semester_gpa": (0, 10),
        "current_gpa": (0, 10),
        "study_hours_per_week": (0, 80),
        "year": (1, 4),
        "semester": (1, 8),
        "stress_level": (1, 10),
        "sleep_hours": (0, 12),
    }
    for key, (lower, upper) in ranges.items():
        if key in payload and not lower <= float(payload[key]) <= upper:
            errors.append(f"{key} must be between {lower} and {upper}")
    for key in ["backlogs", "late_submissions", "lms_login_frequency"]:
        if key in payload and int(payload[key]) < 0:
            errors.append(f"{key} must be 0 or greater")
    return len(errors) == 0, errors


def clean_display_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    display = df.copy()
    return display.fillna("-")
