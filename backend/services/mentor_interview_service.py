from __future__ import annotations

import json
from typing import Any
from uuid import uuid4

from sqlalchemy.orm import Session

from backend.models.mentor_answer import MentorAnswer
from backend.models.mentor_report import MentorReport
from backend.models.mentor_session import MentorSession
from backend.schemas.mentor_schema import MentorAnswerRequest, MentorStartRequest
from backend.services.ai_provider_service import generate_next_question_with_fallback


OPENING_QUESTION = "What kind of work or subjects make you feel most interested right now?"
OPENING_REASON = "This starts with the student's own motivation instead of forcing a fixed career track."


def _loads(value: str | None, default: Any) -> Any:
    if not value:
        return default
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return default


def answer_to_dict(answer: MentorAnswer) -> dict[str, Any]:
    return {
        "question_number": answer.question_number,
        "question_text": answer.question_text,
        "answer_text": answer.answer_text,
        "detected_signals": _loads(answer.detected_signals_json, {}),
        "next_question_reason": answer.next_question_reason,
        "created_at": answer.created_at.isoformat() if answer.created_at else None,
    }


def session_to_dict(db: Session, session: MentorSession) -> dict[str, Any]:
    answers = (
        db.query(MentorAnswer)
        .filter(MentorAnswer.session_id == session.session_id)
        .order_by(MentorAnswer.question_number.asc(), MentorAnswer.id.asc())
        .all()
    )
    return {
        "session_id": session.session_id,
        "student_id": session.student_id,
        "student_name": session.student_name,
        "academic_context": _loads(session.academic_context_json, {}),
        "status": session.status,
        "current_question_number": session.current_question_number,
        "max_questions": session.max_questions,
        "clarity_score": session.clarity_score,
        "dominant_interest_area": session.dominant_interest_area,
        "current_question": session.current_question_text,
        "current_question_reason": session.current_question_reason,
        "answers": [answer_to_dict(answer) for answer in answers],
    }


def start_session(db: Session, payload: MentorStartRequest) -> dict[str, Any]:
    session = MentorSession(
        session_id=f"MENTOR-{uuid4().hex[:12].upper()}",
        student_id=payload.student_id,
        student_name=payload.student_name,
        academic_context_json=json.dumps(payload.academic_context),
        status="active",
        current_question_number=1,
        max_questions=payload.max_questions,
        clarity_score=0.0,
        current_question_text=OPENING_QUESTION,
        current_question_reason=OPENING_REASON,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session_to_dict(db, session)


def get_session(db: Session, session_id: str) -> MentorSession | None:
    return db.query(MentorSession).filter(MentorSession.session_id == session_id).first()


def list_sessions(db: Session) -> list[dict[str, Any]]:
    sessions = db.query(MentorSession).order_by(MentorSession.updated_at.desc(), MentorSession.id.desc()).all()
    return [session_to_dict(db, session) for session in sessions]


def submit_answer(db: Session, session: MentorSession, payload: MentorAnswerRequest) -> dict[str, Any]:
    existing_answers = (
        db.query(MentorAnswer)
        .filter(MentorAnswer.session_id == session.session_id)
        .order_by(MentorAnswer.question_number.asc(), MentorAnswer.id.asc())
        .all()
    )
    answers_for_context = [answer_to_dict(answer) for answer in existing_answers]
    answers_for_context.append(
        {
            "question_number": session.current_question_number,
            "question_text": session.current_question_text,
            "answer_text": payload.answer.strip(),
        }
    )
    context = {
        "session_id": session.session_id,
        "student_id": session.student_id,
        "student_name": session.student_name,
        "academic_context": _loads(session.academic_context_json, {}),
        "max_questions": session.max_questions,
        "answers": answers_for_context,
    }
    result, warning = generate_next_question_with_fallback(context)
    signals = result.get("detected_signals", {})
    analysis = result.get("previous_answer_analysis", {})
    clarity = float(analysis.get("clarity_score") or signals.get("clarity_score") or 0.0)
    interests = signals.get("career_hints") or analysis.get("possible_paths") or signals.get("interests") or []
    dominant = signals.get("recommended_primary_path") or (interests[0] if interests else session.dominant_interest_area)
    ready = bool(result.get("ready_for_report"))

    answer = MentorAnswer(
        session_id=session.session_id,
        question_number=session.current_question_number,
        question_text=session.current_question_text,
        answer_text=payload.answer.strip(),
        detected_signals_json=json.dumps(signals),
        next_question_reason=result.get("why_this_question", ""),
    )
    db.add(answer)

    session.clarity_score = clarity
    session.dominant_interest_area = dominant
    session.status = "ready_for_report" if ready else "active"
    session.current_question_number = min(session.current_question_number + 1, session.max_questions)
    session.current_question_text = result.get("next_question") or "What is the next outcome you want to work toward?"
    session.current_question_reason = result.get("why_this_question") or "This keeps the interview moving toward a practical plan."

    db.commit()
    db.refresh(session)
    return {
        "session_id": session.session_id,
        "status": session.status,
        "current_question_number": session.current_question_number,
        "max_questions": session.max_questions,
        "clarity_score": session.clarity_score,
        "dominant_interest_area": session.dominant_interest_area,
        "previous_answer_analysis": analysis,
        "next_question": session.current_question_text,
        "why_this_question": session.current_question_reason,
        "ready_for_report": ready,
        "provider_warning": warning,
    }


def delete_session(db: Session, session: MentorSession) -> None:
    db.query(MentorReport).filter(MentorReport.session_id == session.session_id).delete()
    db.query(MentorAnswer).filter(MentorAnswer.session_id == session.session_id).delete()
    db.delete(session)
    db.commit()
