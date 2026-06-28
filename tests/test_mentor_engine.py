from __future__ import annotations

from tests.test_api import client


def test_mentor_interview_generates_and_persists_report():
    start = client.post(
        "/mentor/start",
        json={
            "student_id": "MENTOR_TEST_001",
            "student_name": "Mentor Test",
            "max_questions": 12,
            "academic_context": {
                "department": "Computer Science",
                "year": 3,
                "current_gpa": 6.8,
                "attendance_percentage": 72,
                "risk_category": "Medium Risk",
            },
        },
    )

    assert start.status_code == 200
    session = start.json()
    session_id = session["session_id"]
    assert session["current_question"]
    assert session["status"] == "active"

    answers = [
        "I enjoy Python, maths, statistics, and analyzing data to find useful patterns.",
        "I like building machine learning models and explaining charts to classmates.",
        "SQL feels interesting, but I need more practice with project structure.",
        "I prefer project-based learning and want a strong GitHub portfolio.",
        "I can study around two focused hours daily for the next month.",
        "My weak areas are DSA practice and communication polish.",
        "I would be proud to build a student performance analytics dashboard.",
        "My goal is internship readiness with a data science direction.",
    ]

    last = None
    for answer in answers:
        response = client.post(f"/mentor/{session_id}/answer", json={"answer": answer})
        assert response.status_code == 200
        last = response.json()

    assert last is not None
    assert last["ready_for_report"] is True
    assert last["clarity_score"] >= 0.75

    session_response = client.get(f"/mentor/{session_id}")
    assert session_response.status_code == 200
    saved_session = session_response.json()
    assert len(saved_session["answers"]) == 8
    assert saved_session["dominant_interest_area"]

    report_response = client.post(f"/mentor/{session_id}/report")
    assert report_response.status_code == 200
    report_payload = report_response.json()
    report = report_payload["report"]

    expected_sections = {
        "executive_summary",
        "student_profile_summary",
        "academic_risk_analysis",
        "interest_and_strength_analysis",
        "personality_and_work_style",
        "career_path_recommendation",
        "career_reasoning_trace",
        "career_fit_matrix",
        "confidence_breakdown",
        "swot_analysis",
        "skill_gap_analysis",
        "skill_heatmap",
        "readiness_scores",
        "personalized_skill_roadmap",
        "daily_learning_pattern",
        "weekly_plan",
        "one_year_growth_plan",
        "project_recommendations",
        "resource_recommendations",
        "mentor_advice",
        "mistake_warnings",
        "interview_and_resume_direction",
        "parent_or_faculty_summary",
        "mentor_review_questions",
        "follow_up_questions",
    }
    assert expected_sections.issubset(report.keys())
    assert report_payload["primary_career_path"]
    assert report_payload["primary_career_path"] == report["career_path_recommendation"]["primary_path"]
    assert report["career_reasoning_trace"]["final_direction"] == report_payload["primary_career_path"]
    assert len(report["career_fit_matrix"]) >= 5
    assert report_payload["secondary_career_paths"]

    saved_report = client.get(f"/mentor/{session_id}/report")
    assert saved_report.status_code == 200
    assert saved_report.json()["report"] == report


def test_mentor_provider_status_hides_secrets():
    response = client.get("/mentor/provider-status")

    assert response.status_code == 200
    body = response.json()
    assert "API_KEY" not in str(body)
    assert "provider" in body
    assert body["fallback_available"] is True
