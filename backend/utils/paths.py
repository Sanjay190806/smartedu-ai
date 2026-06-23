from __future__ import annotations

from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def resolve_from_root(relative_path: str | Path) -> Path:
    return project_root() / Path(relative_path)
