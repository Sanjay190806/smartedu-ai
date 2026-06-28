from __future__ import annotations

from backend.ai.base import BaseAIProvider
from backend.ai.groq_provider import GroqProvider
from backend.ai.offline_provider import OfflineMentorProvider
from backend.ai.openrouter_provider import OpenRouterProvider
from backend.config import settings


def get_provider() -> BaseAIProvider:
    provider = settings.AI_PROVIDER.strip().lower()
    if provider == "openrouter":
        return OpenRouterProvider()
    if provider == "groq":
        return GroqProvider()
    return OfflineMentorProvider()


def provider_status() -> dict:
    provider = settings.AI_PROVIDER.strip().lower()
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
        if provider != "offline":
            warning = f"Unknown AI provider '{provider}'. Using offline fallback."
    return {
        "provider": provider,
        "real_ai_configured": configured,
        "fallback_available": True,
        "active_model": active_model,
        "provider_warning": warning,
    }
