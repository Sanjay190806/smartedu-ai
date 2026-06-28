from __future__ import annotations

from typing import Any

import requests

from backend.ai.base import BaseAIProvider
from backend.ai.prompt_templates import generate_mentor_report_prompt, generate_next_question_prompt
from backend.ai.response_parser import parse_json_response
from backend.config import settings


GROQ_CHAT_COMPLETIONS_URL = "https://api.groq.com/openai/v1/chat/completions"


class GroqProvider(BaseAIProvider):
    name = "groq"
    model_name = settings.GROQ_MODEL

    def _complete(self, prompt: str) -> dict[str, Any]:
        if not settings.GROQ_API_KEY:
            raise RuntimeError("Groq API key is not configured.")
        try:
            response = requests.post(
                GROQ_CHAT_COMPLETIONS_URL,
                headers={"Authorization": f"Bearer {settings.GROQ_API_KEY}", "Content-Type": "application/json"},
                json={
                    "model": settings.GROQ_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": settings.AI_TEMPERATURE,
                    "max_tokens": settings.AI_MAX_TOKENS,
                },
                timeout=settings.AI_REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            text = response.json()["choices"][0]["message"]["content"]
            return parse_json_response(text)
        except (requests.RequestException, KeyError, IndexError, TypeError, AttributeError, ValueError) as exc:
            raise RuntimeError(f"Groq request failed: {exc}") from exc

    def generate_next_question(self, context: dict[str, Any]) -> dict[str, Any]:
        return self._complete(generate_next_question_prompt(context))

    def generate_report(self, context: dict[str, Any]) -> dict[str, Any]:
        return self._complete(generate_mentor_report_prompt(context))
