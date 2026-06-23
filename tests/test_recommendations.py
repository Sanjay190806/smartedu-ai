from ml.recommendation_engine import generate_recommendations, identify_top_problems


def test_high_risk_recommendations_include_intervention():
    student = {
        "attendance_percentage": 60,
        "assignment_completion_rate": 55,
        "current_gpa": 5.8,
        "backlogs": 2,
        "study_hours_per_week": 5,
        "stress_level": 8,
        "sleep_hours": 5.2,
        "subject_programming_score": 52,
        "subject_math_score": 58,
    }

    plan = generate_recommendations(student, "High Risk")

    assert "Immediate academic support" in plan["summary"]
    assert plan["risk_category"] == "High Risk"
    assert len(plan["action_plan"]) <= 5
    assert plan["top_problems"] == plan["top_3_problems"]
    assert plan["action_plan"] == plan["top_5_actions"]
    assert plan["resources"]
    assert any("mentor" in action.lower() for action in plan["action_plan"])


def test_top_problems_are_personalized():
    student = {
        "attendance_percentage": 90,
        "assignment_completion_rate": 92,
        "current_gpa": 8.4,
        "backlogs": 0,
        "study_hours_per_week": 15,
        "stress_level": 4,
        "sleep_hours": 7.2,
        "subject_programming_score": 84,
        "subject_math_score": 82,
    }

    assert identify_top_problems(student) == []
