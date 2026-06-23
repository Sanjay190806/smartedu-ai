from __future__ import annotations

from fastapi import APIRouter

from backend.services.prediction_service import model_is_available


router = APIRouter(tags=["Health"])


@router.get("/")
def root() -> dict[str, str]:
    return {"message": "SmartEdu AI Backend is running", "docs": "/docs"}


@router.get("/health")
def health_check() -> dict[str, object]:
    return {
        "status": "ok",
        "service": "SmartEdu AI Backend",
        "phase": "2",
        "model_loaded": model_is_available(),
    }
