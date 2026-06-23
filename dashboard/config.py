from __future__ import annotations

import os


APP_TITLE = "SmartEdu AI"
APP_SUBTITLE = "Explainable Student Performance Prediction and Personalized Academic Guidance"
API_BASE_URL = os.getenv("SMARTEDU_API_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
REQUEST_TIMEOUT = 8

RISK_COLORS = {
    "Low Risk": "#15803d",
    "Medium Risk": "#b45309",
    "High Risk": "#b91c1c",
}

PAGE_ICON = "SA"
DISCLAIMER = (
    "SmartEdu AI is an academic support tool. Predictions are probabilistic and should be used "
    "by mentors and educators as guidance, not as a final decision about a student."
)

REQUIRED_STUDENT_COLUMNS = [
    "student_id",
    "name",
    "department",
    "year",
    "semester",
    "gender",
    "attendance_percentage",
    "internal_marks_average",
    "assignment_completion_rate",
    "quiz_average",
    "previous_semester_gpa",
    "current_gpa",
    "study_hours_per_week",
    "backlogs",
    "late_submissions",
    "participation_score",
    "subject_math_score",
    "subject_programming_score",
    "subject_electronics_score",
    "subject_communication_score",
    "subject_lab_score",
    "library_usage_hours",
    "lms_login_frequency",
    "parent_meeting_count",
    "mentor_meeting_count",
    "extracurricular_hours",
    "stress_level",
    "sleep_hours",
    "internet_access",
]
