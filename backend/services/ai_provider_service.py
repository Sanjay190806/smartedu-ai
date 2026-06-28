from __future__ import annotations

from typing import Any

from backend.ai.offline_provider import OfflineMentorProvider
from backend.ai.provider_factory import get_provider, provider_status


def get_mentor_provider_status() -> dict[str, Any]:
    return provider_status()


def get_provider_status() -> dict[str, Any]:
    return get_mentor_provider_status()


def generate_next_question_with_fallback(context: dict[str, Any]) -> tuple[dict[str, Any], str | None]:
    provider = get_provider()
    try:
        result = provider.generate_next_question(context)
        return result, None
    except Exception as exc:
        result = OfflineMentorProvider().generate_next_question(context)
        result["fallback_used"] = True
        return result, f"{provider.name} failed; offline fallback used."


def generate_report_with_fallback(context: dict[str, Any]) -> tuple[dict[str, Any], str | None]:
    provider = get_provider()
    try:
        result = provider.generate_report(context)
        return result, None
    except Exception:
        result = OfflineMentorProvider().generate_report(context)
        result["fallback_used"] = True
        return result, f"{provider.name} failed; offline fallback used."
