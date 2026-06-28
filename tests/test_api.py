import os
import tempfile
import atexit

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

test_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
test_db.close()
os.environ["DATABASE_URL"] = f"sqlite:///{test_db.name}"
os.environ["AI_PROVIDER"] = "offline"

from backend.database import Base, get_db  # noqa: E402
from backend.main import app
from backend.models import academic_record, prediction, recommendation, student  # noqa: F401, E402


engine = create_engine(os.environ["DATABASE_URL"], connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base.metadata.create_all(bind=engine)


def cleanup_test_db() -> None:
    engine.dispose()
    if os.path.exists(test_db.name):
        try:
            os.remove(test_db.name)
        except PermissionError:
            pass


atexit.register(cleanup_test_db)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


VALID_STUDENT = {
    "student_id": "API_TEST_001",
    "name": "Test Student",
    "department": "Computer Science",
    "year": 3,
    "semester": 5,
    "gender": "Female",
    "attendance_percentage": 64,
    "internal_marks_average": 58,
    "assignment_completion_rate": 62,
    "quiz_average": 55,
    "previous_semester_gpa": 6.2,
    "current_gpa": 6.0,
    "study_hours_per_week": 7,
    "backlogs": 1,
    "late_submissions": 4,
    "participation_score": 50,
    "subject_math_score": 57,
    "subject_programming_score": 53,
    "subject_electronics_score": 61,
    "subject_communication_score": 68,
    "subject_lab_score": 60,
    "library_usage_hours": 2.5,
    "lms_login_frequency": 5,
    "parent_meeting_count": 1,
    "mentor_meeting_count": 1,
    "extracurricular_hours": 2,
    "stress_level": 8,
    "sleep_hours": 5.5,
    "internet_access": "Yes",
}


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "SmartEdu AI Backend"


def test_predict_returns_valid_risk_category():
    response = client.post("/predict", json=VALID_STUDENT)

    assert response.status_code == 200
    body = response.json()
    assert body["risk_category"] in {"Low Risk", "Medium Risk", "High Risk"}
    assert 0 <= body["probability"] <= 1
    assert body["recommendations"]["summary"]
    assert body["recommendations"]["resources"]

    recommendation_response = client.get(f"/recommendations/{VALID_STUDENT['student_id']}")
    assert recommendation_response.status_code == 200
    recommendation = recommendation_response.json()
    assert recommendation["resources"] == body["recommendations"]["resources"]
    for key in ["top_problems", "action_plan", "seven_day_plan", "thirty_day_plan", "mentor_note"]:
        assert recommendation[key]


def test_predict_rejects_invalid_data():
    invalid = {**VALID_STUDENT, "attendance_percentage": 140}

    response = client.post("/predict", json=invalid)

    assert response.status_code == 422


def test_analytics_summary_returns_expected_keys():
    response = client.get("/analytics/summary")

    assert response.status_code == 200
    body = response.json()
    expected = {
        "total_students",
        "low_risk_count",
        "medium_risk_count",
        "high_risk_count",
        "average_attendance",
        "average_gpa",
        "average_assignment_completion",
        "top_weak_subjects",
    }
    assert expected.issubset(body.keys())


def test_students_returns_list():
    response = client.get("/students")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_batch_prediction_smoke():
    import pandas as pd

    df = pd.DataFrame([{**VALID_STUDENT, "student_id": "API_BATCH_001"}])
    response = client.post(
        "/predict/batch",
        files={"file": ("batch.csv", df.to_csv(index=False), "text/csv")},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["total_records"] == 1
    assert body["predictions"][0]["student_id"] == "API_BATCH_001"
    assert body["predictions"][0]["recommendations"]["resources"]
