from __future__ import annotations

from typing import Any


def generate_learning_plan(primary_path: str, signals: dict[str, Any], academic_context: dict[str, Any] | None = None) -> dict[str, Any]:
    academic_context = academic_context or {}
    risk = academic_context.get("risk_category", "Unknown")
    daily_time = signals.get("daily_time_hours") or "1.5-2"

    if "Data" in primary_path or "Machine Learning" in primary_path:
        daily = [
            "30 min Python/Pandas practice",
            "30 min SQL or statistics basics",
            "30 min dataset notebook or visualization",
            "15 min revision notes",
        ]
        first_skills = ["Python data handling", "SQL", "statistics basics", "visualization"]
    elif "Embedded" in primary_path or "IoT" in primary_path:
        daily = [
            "30 min C/Embedded C basics",
            "30 min sensor or Arduino practice",
            "20 min electronics concept revision",
            "30 min prototype/project logging",
        ]
        first_skills = ["C basics", "microcontrollers", "sensors", "IoT data flow"]
    elif "Product" in primary_path or "Business" in primary_path:
        daily = [
            "30 min SQL or Excel practice",
            "30 min product/business case analysis",
            "20 min communication/storytelling",
            "30 min dashboard or PRD work",
        ]
        first_skills = ["SQL", "metrics", "communication", "case thinking"]
    else:
        daily = [
            "45 min DSA/problem solving",
            "30 min backend/API or app building",
            "20 min CS fundamentals",
            "20 min Git/project work",
        ]
        first_skills = ["DSA", "APIs", "databases", "Git"]

    return {
        "available_daily_time": daily_time,
        "risk_context": risk,
        "skills_to_improve_first": first_skills,
        "daily_learning_pattern": {
            "recommended_daily_schedule": daily,
            "minimum_non_zero_day_plan": "Spend 20 minutes on one small topic, one practice task, or one revision note.",
            "deep_work_block": "Use one 90-minute block for the hardest skill before entertainment or distractions.",
            "revision_pattern": "Revise yesterday's notes for 10-15 minutes before starting new work.",
            "practice_pattern": "Practice through small outputs, not only videos.",
            "weekend_project_pattern": "Use weekends for one visible GitHub/project deliverable.",
        },
        "weekly_plan": {
            "monday": ["Core skill practice", "Short revision"],
            "tuesday": ["Tool practice", "One small exercise"],
            "wednesday": ["Project work", "Document learnings"],
            "thursday": ["Weak area repair", "Mentor/peer doubt clearing"],
            "friday": ["Practice test or project checkpoint"],
            "saturday": ["Long project block", "GitHub update"],
            "sunday": ["Review week", "Plan next week", "Rest and reset"],
        },
        "roadmap": {
            "next_30_days": first_skills[:2] + ["Build one mini project"],
            "next_60_days": first_skills + ["Publish one portfolio project"],
            "next_90_days": ["Second project", "Resume update", "Mock interview preparation"],
            "six_month_direction": ["Two strong projects", "Interview-ready fundamentals", "Clear portfolio story"],
        },
    }
