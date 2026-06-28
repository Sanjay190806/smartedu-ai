from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from backend.models.mentor_answer import MentorAnswer
from backend.models.mentor_report import MentorReport
from backend.models.mentor_session import MentorSession
from backend.services.ai_provider_service import generate_report_with_fallback
from backend.services.mentor_interview_service import _loads, answer_to_dict


def _secondary_paths(report: dict[str, Any]) -> list[dict[str, Any]]:
    recommendation = report.get("career_path_recommendation", {})
    return recommendation.get("secondary_paths", [])


def _report_to_dict(report_model: MentorReport, warning: str | None = None) -> dict[str, Any]:
    return {
        "session_id": report_model.session_id,
        "student_id": report_model.student_id,
        "primary_career_path": report_model.primary_career_path,
        "secondary_career_paths": _loads(report_model.secondary_career_paths_json, []),
        "confidence_score": report_model.confidence_score,
        "report": _loads(report_model.report_json, {}),
        "provider_warning": warning,
    }


def get_saved_report(db: Session, session_id: str) -> MentorReport | None:
    return db.query(MentorReport).filter(MentorReport.session_id == session_id).first()


def generate_report(db: Session, session: MentorSession) -> dict[str, Any]:
    answers = (
        db.query(MentorAnswer)
        .filter(MentorAnswer.session_id == session.session_id)
        .order_by(MentorAnswer.question_number.asc(), MentorAnswer.id.asc())
        .all()
    )
    if not answers:
        raise ValueError("Mentor report requires at least one interview answer.")

    context = {
        "session_id": session.session_id,
        "student_id": session.student_id,
        "student_name": session.student_name,
        "academic_context": _loads(session.academic_context_json, {}),
        "answers": [answer_to_dict(answer) for answer in answers],
    }
    report, warning = generate_report_with_fallback(context)
    recommendation = report.get("career_path_recommendation", {})
    profile = report.get("student_profile_summary", {})
    primary_path = recommendation.get("primary_path") or "Career Exploration"
    secondary_paths = _secondary_paths(report)
    confidence = float(profile.get("confidence_score") or session.clarity_score or 0.5)

    saved = get_saved_report(db, session.session_id)
    if saved is None:
        saved = MentorReport(session_id=session.session_id, student_id=session.student_id)
        db.add(saved)
    saved.student_id = session.student_id
    saved.report_json = json.dumps(report)
    saved.primary_career_path = primary_path
    saved.secondary_career_paths_json = json.dumps(secondary_paths)
    saved.confidence_score = confidence

    session.status = "completed"
    session.dominant_interest_area = primary_path
    session.clarity_score = max(session.clarity_score, min(confidence, 0.95))
    session.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(saved)
    return _report_to_dict(saved, warning)


def report_to_dict(report_model: MentorReport) -> dict[str, Any]:
    return _report_to_dict(report_model)
