from __future__ import annotations

from datetime import datetime
from typing import Any

from dashboard.components.theme import get_risk_colors


def safe_get(data: dict[str, Any] | None, key: str, default: Any = "-") -> Any:
    if not isinstance(data, dict):
        return default
    value = data.get(key, default)
    return default if value is None else value


def format_percentage(value: Any) -> str:
    try:
        return f"{float(value):.1f}%"
    except (TypeError, ValueError):
        return "-"


def format_gpa(value: Any) -> str:
    try:
        return f"{float(value):.2f}/10"
    except (TypeError, ValueError):
        return "-"


def format_probability(value: Any) -> str:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return "-"
    if numeric <= 1:
        numeric *= 100
    return f"{numeric:.1f}%"


def format_datetime(value: Any) -> str:
    if not value:
        return "-"
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M")
    text = str(value).replace("T", " ")
    return text[:16]


def risk_label_to_color(risk: str) -> str:
    return get_risk_colors().get(risk, "#475569")
