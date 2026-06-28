from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

from backend.utils.paths import resolve_from_root


load_dotenv(resolve_from_root(".env"))


def _get_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default


def _get_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default


def _normalize_provider(value: str | None) -> str:
    provider = (value or "groq").strip().lower()
    if provider in {"groq", "openrouter", "offline"}:
        return provider
    return "offline"


@dataclass(frozen=True)
class Settings:
    PROJECT_NAME: str = "SmartEdu AI Backend"
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./smartedu.db")
    MODEL_PATH: str = os.getenv("MODEL_PATH", "ml/model_registry/model.joblib")
    PREPROCESSOR_PATH: str = os.getenv("PREPROCESSOR_PATH", "ml/model_registry/preprocessor.joblib")
    FEATURE_NAMES_PATH: str = os.getenv("FEATURE_NAMES_PATH", "ml/model_registry/feature_names.json")
    METRICS_PATH: str = os.getenv("METRICS_PATH", "ml/model_registry/metrics.json")
    SAMPLE_DATA_PATH: str = os.getenv("SAMPLE_DATA_PATH", "data/sample_students.csv")
    AI_PROVIDER: str = _normalize_provider(os.getenv("AI_PROVIDER", "groq"))
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
    AI_REQUEST_TIMEOUT: int = _get_int("AI_REQUEST_TIMEOUT", 30)
    AI_MAX_TOKENS: int = _get_int("AI_MAX_TOKENS", 1800)
    AI_TEMPERATURE: float = _get_float("AI_TEMPERATURE", 0.4)

    @property
    def model_path(self):
        return resolve_from_root(self.MODEL_PATH)

    @property
    def preprocessor_path(self):
        return resolve_from_root(self.PREPROCESSOR_PATH)

    @property
    def feature_names_path(self):
        return resolve_from_root(self.FEATURE_NAMES_PATH)

    @property
    def metrics_path(self):
        return resolve_from_root(self.METRICS_PATH)

    @property
    def sample_data_path(self):
        return resolve_from_root(self.SAMPLE_DATA_PATH)


settings = Settings()
