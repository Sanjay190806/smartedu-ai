from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.analytics_schema import AnalyticsSummary, SubjectPerformance
from backend.services.analytics_service import (
    analytics_summary,
    department_analytics,
    risk_distribution,
    subject_performance,
)


router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary", response_model=AnalyticsSummary)
def summary(db: Session = Depends(get_db)):
    return analytics_summary(db)


@router.get("/risk-distribution")
def distribution(db: Session = Depends(get_db)):
    return risk_distribution(db)


@router.get("/department/{department}")
def department(department: str, db: Session = Depends(get_db)):
    return department_analytics(db, department)


@router.get("/subject-performance", response_model=SubjectPerformance)
def subjects(db: Session = Depends(get_db)):
    return subject_performance(db)
