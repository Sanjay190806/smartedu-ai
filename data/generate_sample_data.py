from __future__ import annotations

from pathlib import Path
import random

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = PROJECT_ROOT / "data" / "sample_students.csv"
RANDOM_SEED = 42

DEPARTMENTS = [
    "Computer Science",
    "Information Technology",
    "Electronics",
    "Mechanical",
    "Civil",
    "Data Science",
]
GENDERS = ["Female", "Male", "Non-binary"]
FIRST_NAMES = [
    "Aarav", "Aditi", "Ananya", "Arjun", "Diya", "Ishaan", "Kavya", "Meera",
    "Neha", "Rohan", "Saanvi", "Sanjay", "Tara", "Vihaan", "Zoya", "Nikhil",
    "Priya", "Rahul", "Sneha", "Varun",
]
LAST_NAMES = [
    "Sharma", "Patel", "Reddy", "Iyer", "Nair", "Gupta", "Khan", "Das",
    "Mehta", "Rao", "Verma", "Joshi", "Menon", "Chopra", "Kapoor",
]


def clamp(value: float, lower: float, upper: float) -> float:
    return float(max(lower, min(upper, value)))


def score_to_risk_label(row: dict[str, float | int | str]) -> str:
    """Create logical labels from academic and wellbeing signals."""
    risk_score = 0

    if row["attendance_percentage"] < 65:
        risk_score += 3
    elif row["attendance_percentage"] < 75:
        risk_score += 2
    elif row["attendance_percentage"] < 82:
        risk_score += 1

    if row["current_gpa"] < 6.0:
        risk_score += 3
    elif row["current_gpa"] < 7.0:
        risk_score += 2
    elif row["current_gpa"] < 7.8:
        risk_score += 1

    if row["internal_marks_average"] < 55:
        risk_score += 3
    elif row["internal_marks_average"] < 68:
        risk_score += 2

    if row["assignment_completion_rate"] < 60:
        risk_score += 3
    elif row["assignment_completion_rate"] < 75:
        risk_score += 2

    if row["backlogs"] >= 3:
        risk_score += 4
    elif row["backlogs"] >= 1:
        risk_score += 2

    if row["study_hours_per_week"] < 6:
        risk_score += 2
    elif row["study_hours_per_week"] < 10:
        risk_score += 1

    if row["stress_level"] >= 8:
        risk_score += 2
    elif row["stress_level"] >= 6:
        risk_score += 1

    if row["sleep_hours"] < 5.5:
        risk_score += 2
    elif row["sleep_hours"] < 6.5:
        risk_score += 1

    weak_subjects = sum(
        row[column] < 60
        for column in [
            "subject_math_score",
            "subject_programming_score",
            "subject_electronics_score",
            "subject_communication_score",
            "subject_lab_score",
        ]
    )
    risk_score += min(weak_subjects, 3)

    risk_score += random.choice([-1, 0, 0, 0, 1])

    if risk_score >= 11:
        return "High Risk"
    if risk_score >= 6:
        return "Medium Risk"
    return "Low Risk"


def build_student(index: int) -> dict[str, object]:
    performance_band = random.choices(
        ["strong", "average", "struggling"], weights=[0.38, 0.42, 0.20], k=1
    )[0]

    if performance_band == "strong":
        attendance = np.random.normal(88, 6)
        gpa = np.random.normal(8.4, 0.6)
        marks = np.random.normal(82, 7)
        assignment = np.random.normal(90, 6)
        study_hours = np.random.normal(16, 4)
        backlogs = random.choices([0, 1], weights=[0.92, 0.08], k=1)[0]
        stress = np.random.normal(4, 1.3)
        sleep = np.random.normal(7.2, 0.7)
    elif performance_band == "average":
        attendance = np.random.normal(78, 9)
        gpa = np.random.normal(7.2, 0.8)
        marks = np.random.normal(68, 9)
        assignment = np.random.normal(76, 10)
        study_hours = np.random.normal(10, 4)
        backlogs = random.choices([0, 1, 2], weights=[0.68, 0.24, 0.08], k=1)[0]
        stress = np.random.normal(5.8, 1.5)
        sleep = np.random.normal(6.5, 0.8)
    else:
        attendance = np.random.normal(62, 11)
        gpa = np.random.normal(5.8, 0.9)
        marks = np.random.normal(54, 10)
        assignment = np.random.normal(58, 13)
        study_hours = np.random.normal(6, 3)
        backlogs = random.choices([0, 1, 2, 3, 4], weights=[0.18, 0.28, 0.25, 0.18, 0.11], k=1)[0]
        stress = np.random.normal(7.5, 1.4)
        sleep = np.random.normal(5.5, 0.9)

    current_gpa = round(clamp(gpa, 4.0, 10.0), 2)
    previous_gpa = round(clamp(current_gpa + np.random.normal(0, 0.45), 4.0, 10.0), 2)
    attendance_percentage = round(clamp(attendance, 35, 100), 1)
    internal_marks_average = round(clamp(marks, 25, 100), 1)
    assignment_completion_rate = round(clamp(assignment, 20, 100), 1)

    base_subject = internal_marks_average + np.random.normal(0, 5)
    row: dict[str, object] = {
        "student_id": f"SE{index:04d}",
        "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
        "department": random.choice(DEPARTMENTS),
        "year": random.randint(1, 4),
        "semester": random.randint(1, 8),
        "gender": random.choice(GENDERS),
        "attendance_percentage": attendance_percentage,
        "internal_marks_average": internal_marks_average,
        "assignment_completion_rate": assignment_completion_rate,
        "quiz_average": round(clamp(internal_marks_average + np.random.normal(0, 8), 20, 100), 1),
        "previous_semester_gpa": previous_gpa,
        "current_gpa": current_gpa,
        "study_hours_per_week": round(clamp(study_hours, 1, 35), 1),
        "backlogs": int(backlogs),
        "late_submissions": int(clamp(np.random.poisson(max(0.5, (100 - assignment_completion_rate) / 18)), 0, 12)),
        "participation_score": round(clamp(internal_marks_average + np.random.normal(0, 12), 15, 100), 1),
        "subject_math_score": round(clamp(base_subject + np.random.normal(0, 10), 20, 100), 1),
        "subject_programming_score": round(clamp(base_subject + np.random.normal(0, 11), 20, 100), 1),
        "subject_electronics_score": round(clamp(base_subject + np.random.normal(0, 10), 20, 100), 1),
        "subject_communication_score": round(clamp(base_subject + np.random.normal(3, 9), 20, 100), 1),
        "subject_lab_score": round(clamp(base_subject + np.random.normal(4, 9), 20, 100), 1),
        "library_usage_hours": round(clamp(np.random.normal(study_hours / 3, 2), 0, 18), 1),
        "lms_login_frequency": int(clamp(np.random.normal(study_hours * 0.9, 4), 0, 35)),
        "parent_meeting_count": int(clamp(np.random.poisson(0.8 if performance_band != "struggling" else 1.6), 0, 6)),
        "mentor_meeting_count": int(clamp(np.random.poisson(1.4 if performance_band != "strong" else 0.8), 0, 8)),
        "extracurricular_hours": round(clamp(np.random.normal(4, 3), 0, 18), 1),
        "stress_level": int(round(clamp(stress, 1, 10))),
        "sleep_hours": round(clamp(sleep, 3.5, 9.5), 1),
        "internet_access": random.choices(["Yes", "No"], weights=[0.88, 0.12], k=1)[0],
    }
    row["risk_label"] = score_to_risk_label(row)
    return row


def generate_dataset(record_count: int = 300) -> pd.DataFrame:
    random.seed(RANDOM_SEED)
    np.random.seed(RANDOM_SEED)
    return pd.DataFrame([build_student(index) for index in range(1, record_count + 1)])


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    dataset = generate_dataset(300)
    dataset.to_csv(OUTPUT_PATH, index=False)
    print(f"Generated {len(dataset)} records at {OUTPUT_PATH}")
    print(dataset["risk_label"].value_counts().to_string())


if __name__ == "__main__":
    main()
