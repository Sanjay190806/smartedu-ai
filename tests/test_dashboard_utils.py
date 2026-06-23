import pandas as pd

from dashboard import api_client
from dashboard.config import REQUIRED_STUDENT_COLUMNS
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
