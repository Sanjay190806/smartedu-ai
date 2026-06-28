from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.mentor_schema import (
    MentorAnswerRequest,
    MentorAnswerResponse,
    MentorReportResponse,
    MentorSessionResponse,
    MentorStartRequest,
)
from backend.services.ai_provider_service import get_mentor_provider_status
from backend.services.mentor_interview_service import (
    delete_session,
    get_session,
    list_sessions,
    session_to_dict,
    start_session,
    submit_answer,
)
from backend.services.mentor_report_service import generate_report, get_saved_report, report_to_dict


router = APIRouter(prefix="/mentor", tags=["AI Mentor"])


@router.get("/provider-status")
def provider_status() -> dict:
    return get_mentor_provider_status()


@router.get("/sessions", response_model=list[MentorSessionResponse])
def get_sessions(db: Session = Depends(get_db)):
    return list_sessions(db)


@router.post("/start", response_model=MentorSessionResponse)
def start_mentor_session(payload: MentorStartRequest, db: Session = Depends(get_db)):
    return start_session(db, payload)


@router.post("/{session_id}/answer", response_model=MentorAnswerResponse)
def answer_mentor_question(session_id: str, payload: MentorAnswerRequest, db: Session = Depends(get_db)):
    session = get_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Mentor session not found")
    if session.status == "completed":
        raise HTTPException(status_code=400, detail="Mentor session is already completed")
    return submit_answer(db, session, payload)


@router.get("/{session_id}", response_model=MentorSessionResponse)
def get_mentor_session(session_id: str, db: Session = Depends(get_db)):
    session = get_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Mentor session not found")
    return session_to_dict(db, session)


@router.post("/{session_id}/report", response_model=MentorReportResponse)
def create_mentor_report(session_id: str, db: Session = Depends(get_db)):
    session = get_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Mentor session not found")
    try:
        return generate_report(db, session)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{session_id}/report", response_model=MentorReportResponse)
def get_mentor_report(session_id: str, db: Session = Depends(get_db)):
    report = get_saved_report(db, session_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Mentor report not found")
    return report_to_dict(report)


@router.delete("/{session_id}")
def delete_mentor_session(session_id: str, db: Session = Depends(get_db)):
    session = get_session(db, session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Mentor session not found")
    delete_session(db, session)
    return {"message": "Mentor session deleted", "session_id": session_id}
