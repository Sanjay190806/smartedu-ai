from __future__ import annotations

from backend.ai.base import BaseAIProvider
from backend.ai.groq_provider import GroqProvider
from backend.ai.offline_provider import OfflineMentorProvider
from backend.ai.openrouter_provider import OpenRouterProvider
from backend.config import settings


VALID_PROVIDERS = {"groq", "openrouter", "offline"}


def _normalized_provider() -> str:
    provider = settings.AI_PROVIDER.strip().lower()
    return provider if provider in VALID_PROVIDERS else "offline"


def get_provider() -> BaseAIProvider:
    provider = _normalized_provider()
    if provider == "openrouter":
        return OpenRouterProvider()
    if provider == "groq":
        return GroqProvider()
    return OfflineMentorProvider()


def provider_status() -> dict:
    raw_provider = settings.AI_PROVIDER.strip().lower()
    provider = _normalized_provider()
    warning = None
    if provider == "openrouter":
        configured = bool(settings.OPENROUTER_API_KEY)
        active_model = settings.OPENROUTER_MODEL if configured else "offline-rule-based"
        if not configured:
            warning = "OpenRouter API key is missing. Using offline fallback."
    elif provider == "groq":
        configured = bool(settings.GROQ_API_KEY)
        active_model = settings.GROQ_MODEL if configured else "offline-rule-based"
        if not configured:
            warning = "Groq API key is missing. Using offline fallback."
    else:
        configured = False
        active_model = "offline-rule-based"
        if raw_provider != "offline":
            warning = f"Unknown AI provider '{raw_provider}'. Using offline fallback."
    return {
        "provider": provider,
        "real_ai_configured": configured,
        "fallback_available": True,
        "active_model": active_model,
        "provider_warning": warning,
    }
