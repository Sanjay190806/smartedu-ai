from __future__ import annotations

from typing import Any

from backend.services import ai_provider_service
from backend.ai import groq_provider
from backend.ai.groq_provider import GROQ_CHAT_COMPLETIONS_URL, GroqProvider
from backend.ai.offline_provider import OfflineMentorProvider
from backend.ai import provider_factory
from backend.config import Settings


class FailingProvider:
    name = "failing-test-provider"

    def generate_next_question(self, context: dict[str, Any]) -> dict[str, Any]:
        raise RuntimeError("provider unavailable")

    def generate_report(self, context: dict[str, Any]) -> dict[str, Any]:
        raise RuntimeError("provider unavailable")


def test_next_question_uses_offline_fallback(monkeypatch):
    monkeypatch.setattr(ai_provider_service, "get_provider", lambda: FailingProvider())

    result, warning = ai_provider_service.generate_next_question_with_fallback(
        {
            "answers": [
                {
                    "question_text": "What do you enjoy?",
                    "answer_text": "I like Python, maths, data analysis, and machine learning projects.",
                }
            ],
            "max_questions": 15,
        }
    )

    assert warning == "failing-test-provider failed; offline fallback used."
    assert result["fallback_used"] is True
    assert result["next_question"]
    assert "Data" in " ".join(result["previous_answer_analysis"]["possible_paths"])


def test_report_uses_offline_fallback(monkeypatch):
    monkeypatch.setattr(ai_provider_service, "get_provider", lambda: FailingProvider())

    result, warning = ai_provider_service.generate_report_with_fallback(
        {
            "student_id": "MENTOR_TEST_001",
            "student_name": "Mentor Test",
            "academic_context": {"department": "Computer Science", "risk_category": "Medium Risk"},
            "answers": [
                {"question_text": "Q1", "answer_text": "I like Python and data analysis."},
                {"question_text": "Q2", "answer_text": "I enjoy statistics and dashboards."},
            ],
        }
    )

    assert warning == "failing-test-provider failed; offline fallback used."
    assert result["fallback_used"] is True
    assert result["career_path_recommendation"]["primary_path"]
    assert result["personalized_skill_roadmap"]


def test_provider_status_openrouter_missing_key(monkeypatch):
    monkeypatch.setattr(
        provider_factory,
        "settings",
        Settings(AI_PROVIDER="openrouter", OPENROUTER_API_KEY="", OPENROUTER_MODEL="openai/gpt-4o-mini"),
    )

    status = ai_provider_service.get_provider_status()

    assert status == {
        "provider": "openrouter",
        "real_ai_configured": False,
        "fallback_available": True,
        "active_model": "offline-rule-based",
        "provider_warning": "OpenRouter API key is missing. Using offline fallback.",
    }


def test_provider_status_groq_missing_key(monkeypatch):
    monkeypatch.setattr(
        provider_factory,
        "settings",
        Settings(AI_PROVIDER="groq", GROQ_API_KEY="", GROQ_MODEL="llama-3.1-8b-instant"),
    )

    status = ai_provider_service.get_provider_status()

    assert status == {
        "provider": "groq",
        "real_ai_configured": False,
        "fallback_available": True,
        "active_model": "offline-rule-based",
        "provider_warning": "Groq API key is missing. Using offline fallback.",
    }
    assert "GROQ_API_KEY" not in str(status)


def test_groq_provider_uses_expected_chat_completions_endpoint(monkeypatch):
    captured = {}

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"choices": [{"message": {"content": "{\"ok\": true}"}}]}

    def fake_post(url, **kwargs):
        captured["url"] = url
        captured["kwargs"] = kwargs
        return FakeResponse()

    monkeypatch.setattr(
        groq_provider,
        "settings",
        Settings(
            AI_PROVIDER="groq",
            GROQ_API_KEY="test-placeholder-key",
            GROQ_MODEL="llama-3.1-8b-instant",
            AI_REQUEST_TIMEOUT=7,
        ),
    )
    monkeypatch.setattr(groq_provider.requests, "post", fake_post)

    result = GroqProvider()._complete("Return JSON.")

    assert result == {"ok": True}
    assert captured["url"] == GROQ_CHAT_COMPLETIONS_URL
    assert captured["kwargs"]["json"]["model"] == "llama-3.1-8b-instant"
    assert captured["kwargs"]["timeout"] == 7
    assert captured["kwargs"]["headers"]["Authorization"] == "Bearer test-placeholder-key"


def test_groq_malformed_json_uses_offline_fallback(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"choices": [{"message": {"content": "not valid json"}}]}

    monkeypatch.setattr(
        groq_provider,
        "settings",
        Settings(AI_PROVIDER="groq", GROQ_API_KEY="test-placeholder-key", GROQ_MODEL="llama-3.1-8b-instant"),
    )
    monkeypatch.setattr(groq_provider.requests, "post", lambda *args, **kwargs: FakeResponse())
    monkeypatch.setattr(ai_provider_service, "get_provider", lambda: GroqProvider())

    result, warning = ai_provider_service.generate_next_question_with_fallback(
        {
            "answers": [{"question_text": "Q1", "answer_text": "I like Python and data analytics."}],
            "max_questions": 12,
        }
    )

    assert warning == "groq failed; offline fallback used."
    assert result["fallback_used"] is True
    assert result["next_question"]


def test_groq_timeout_uses_offline_fallback(monkeypatch):
    def timeout_post(*args, **kwargs):
        raise groq_provider.requests.Timeout("timed out")

    monkeypatch.setattr(
        groq_provider,
        "settings",
        Settings(AI_PROVIDER="groq", GROQ_API_KEY="test-placeholder-key", GROQ_MODEL="llama-3.1-8b-instant"),
    )
    monkeypatch.setattr(groq_provider.requests, "post", timeout_post)
    monkeypatch.setattr(ai_provider_service, "get_provider", lambda: GroqProvider())

    result, warning = ai_provider_service.generate_report_with_fallback(
        {
            "student_id": "GROQ_TIMEOUT_TEST",
            "student_name": "Groq Timeout Test",
            "academic_context": {"department": "Computer Science", "risk_category": "Medium Risk"},
            "answers": [{"question_text": "Q1", "answer_text": "I like Python, SQL, and dashboards."}],
        }
    )

    assert warning == "groq failed; offline fallback used."
    assert result["fallback_used"] is True
    assert result["career_path_recommendation"]["primary_path"]


def test_offline_provider_generates_expanded_report_sections():
    provider = OfflineMentorProvider()
    report = provider.generate_report(
        {
            "student_id": "OFFLINE_REPORT_TEST",
            "student_name": "Offline Test",
            "academic_context": {
                "department": "Electronics",
                "year": 3,
                "current_gpa": 6.9,
                "attendance_percentage": 74,
                "risk_category": "Medium Risk",
            },
            "answers": [
                {"question_text": "Q1", "answer_text": "I like Python, maths, and data analysis. I don't like hardware much."},
                {"question_text": "Q2", "answer_text": "I enjoy SQL, statistics, dashboards, and project based learning."},
                {"question_text": "Q3", "answer_text": "I can study 2 hours daily and want internship readiness."},
            ],
        }
    )

    for key in [
        "executive_summary",
        "career_fit_matrix",
        "confidence_breakdown",
        "swot_analysis",
        "skill_heatmap",
        "readiness_scores",
        "one_year_growth_plan",
        "career_reasoning_trace",
    ]:
        assert key in report
    assert report["career_path_recommendation"]["primary_path"] == report["career_reasoning_trace"]["final_direction"]
    assert len(report["career_fit_matrix"]) >= 5
