from __future__ import annotations

from typing import Any

import requests

from backend.ai.base import BaseAIProvider
from backend.ai.offline_provider import OfflineMentorProvider
from backend.ai.prompt_templates import generate_mentor_report_prompt, generate_next_question_prompt
from backend.ai.response_parser import parse_json_response
from backend.config import settings


OPENROUTER_CHAT_COMPLETIONS_URL = "https://openrouter.ai/api/v1/chat/completions"


class OpenRouterProvider(BaseAIProvider):
    name = "openrouter"
    model_name = settings.OPENROUTER_MODEL

    def __init__(self) -> None:
        self.fallback = OfflineMentorProvider()

    def _complete(self, prompt: str) -> dict[str, Any]:
        if not settings.OPENROUTER_API_KEY:
            raise RuntimeError("OpenRouter API key is not configured.")
        try:
            response = requests.post(
                OPENROUTER_CHAT_COMPLETIONS_URL,
                headers={"Authorization": f"Bearer {settings.OPENROUTER_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": settings.OPENROUTER_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": settings.AI_TEMPERATURE,
                    "max_tokens": settings.AI_MAX_TOKENS,
                },
                timeout=settings.AI_REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            payload = response.json()
            text = payload["choices"][0]["message"]["content"]
            return parse_json_response(text)
        except (requests.RequestException, KeyError, IndexError, ValueError, TypeError, AttributeError) as exc:
            raise RuntimeError(f"OpenRouter request failed: {exc}") from exc

    def generate_next_question(self, context: dict[str, Any]) -> dict[str, Any]:
        return self._complete(generate_next_question_prompt(context))

    def generate_report(self, context: dict[str, Any]) -> dict[str, Any]:
        return self._complete(generate_mentor_report_prompt(context))
