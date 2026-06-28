from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseAIProvider(ABC):
    name = "base"
    model_name = "base"

    @abstractmethod
    def generate_next_question(self, context: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def generate_report(self, context: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError
