from __future__ import annotations

import os
from dataclasses import dataclass

from backend.utils.paths import resolve_from_root


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
