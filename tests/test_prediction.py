import pytest

from ml.predict import predict_student_risk


def test_prediction_output_shape():
    student = {
        "student_id": "TEST001",
        "department": "Computer Science",
        "year": 3,
        "semester": 5,
        "gender": "Female",
        "attendance_percentage": 61,
        "internal_marks_average": 54,
        "assignment_completion_rate": 57,
        "quiz_average": 50,
        "previous_semester_gpa": 6.0,
        "current_gpa": 5.7,
        "study_hours_per_week": 5,
        "backlogs": 2,
        "late_submissions": 6,
        "participation_score": 42,
        "subject_math_score": 52,
        "subject_programming_score": 48,
        "subject_electronics_score": 56,
        "subject_communication_score": 63,
        "subject_lab_score": 55,
        "library_usage_hours": 1.5,
        "lms_login_frequency": 4,
        "parent_meeting_count": 1,
        "mentor_meeting_count": 1,
        "extracurricular_hours": 2,
        "stress_level": 8,
        "sleep_hours": 5.0,
        "internet_access": "Yes",
    }

    try:
        result = predict_student_risk(student)
    except FileNotFoundError:
        pytest.skip("Model artifacts not trained yet")

    assert result["risk_category"] in {"Low Risk", "Medium Risk", "High Risk"}
    assert 0 <= result["probability"] <= 1
    assert result["confidence"] in {"Low", "Medium", "High"}
    assert "recommendations" in result
