import pandas as pd

from dashboard import api_client
from dashboard.components.theme import get_plotly_template, get_risk_colors, set_active_theme
from dashboard.config import REQUIRED_STUDENT_COLUMNS
from dashboard.utils.report_export import mentor_report_to_markdown, mentor_report_to_text
from dashboard.utils.formatters import format_gpa, format_percentage, format_probability
from dashboard.utils.sample_payloads import HIGH_RISK_SAMPLE, LOW_RISK_SAMPLE, MEDIUM_RISK_SAMPLE
from dashboard.utils.validators import get_missing_columns, validate_csv_columns, validate_student_payload


def test_sample_payloads_contain_required_fields():
    for payload in [HIGH_RISK_SAMPLE, MEDIUM_RISK_SAMPLE, LOW_RISK_SAMPLE]:
        assert set(REQUIRED_STUDENT_COLUMNS).issubset(payload.keys())
        valid, errors = validate_student_payload(payload)
        assert valid, errors


def test_csv_validator_catches_missing_columns():
    df = pd.DataFrame([{"student_id": "S1", "name": "Student"}])

    valid, missing = validate_csv_columns(df)

    assert not valid
    assert "attendance_percentage" in missing
    assert get_missing_columns(df) == missing


def test_formatters():
    assert format_percentage(81.234) == "81.2%"
    assert format_gpa(7.456) == "7.46/10"
    assert format_probability(0.875) == "87.5%"


def test_api_client_handles_backend_offline(monkeypatch):
    def raise_connection_error(*args, **kwargs):
        raise api_client.requests.ConnectionError("offline")

    monkeypatch.setattr(api_client.requests, "request", raise_connection_error)

    result = api_client.check_backend_health()

    assert result["ok"] is False
    assert "Backend is not running" in result["error"]


def test_theme_helpers_support_light_and_dark():
    assert set_active_theme("Light") == "light"
    assert get_plotly_template() == "plotly_white"
    assert get_risk_colors()["High Risk"] == "#b91c1c"

    assert set_active_theme("Dark") == "dark"
    assert get_plotly_template() == "plotly_dark"
    assert get_risk_colors()["High Risk"] == "#ef4444"


def test_mentor_report_markdown_and_text_exports_are_readable():
    payload = {
        "session_id": "MENTOR_EXPORT_TEST",
        "primary_career_path": "Data Scientist",
        "report": {
            "executive_summary": {"one_paragraph_summary": "Focused data path with Python and SQL."},
            "career_path_recommendation": {
                "primary_path": "Data Scientist",
                "why_this_path_fits": "Repeated Python, maths, and data signals.",
            },
            "skill_gap_analysis": {
                "current_known_skills": ["Python"],
                "skills_to_improve_first": ["SQL", "Statistics"],
            },
            "personalized_skill_roadmap": {
                "next_30_days": ["SQL basics"],
                "next_90_days": ["Portfolio project"],
            },
            "weekly_plan": {"monday": ["SQL practice"]},
            "project_recommendations": [{"project_title": "Analytics Dashboard", "why_this_project": "Portfolio proof"}],
            "mentor_advice": {
                "short_advice": "Build one project.",
                "hard_truth": "Avoid course collecting.",
                "next_best_action": "Practice SQL",
            },
        },
    }

    markdown = mentor_report_to_markdown(payload)
    text = mentor_report_to_text(payload)

    assert "# SmartEdu AI Mentor Report" in markdown
    assert "## Career Recommendation" in markdown
    assert "Data Scientist" in markdown
    assert "SmartEdu AI Mentor Report" in text
