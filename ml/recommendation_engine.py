from __future__ import annotations

from typing import Any


def _value(student: dict[str, Any], key: str, default: float = 0) -> float:
    value = student.get(key, default)
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def identify_top_problems(student: dict[str, Any]) -> list[str]:
    problems: list[tuple[int, str]] = []
    checks = [
        (_value(student, "attendance_percentage") < 75, 5, "Attendance is below the expected 75% level."),
        (_value(student, "assignment_completion_rate") < 70, 5, "Assignment completion is inconsistent."),
        (_value(student, "current_gpa") < 7, 5, "Current GPA needs focused improvement."),
        (_value(student, "backlogs") > 0, 5, "Backlogs need a structured clearing plan."),
        (_value(student, "study_hours_per_week") < 10, 4, "Weekly study hours are lower than recommended."),
        (_value(student, "stress_level") >= 7, 4, "Stress level is high and may affect learning."),
        (_value(student, "sleep_hours") < 6, 3, "Sleep is below a healthy academic routine."),
        (_value(student, "subject_programming_score") < 60, 3, "Programming score needs practice."),
        (_value(student, "subject_math_score") < 60, 3, "Math fundamentals need revision."),
    ]
    for failed, priority, message in checks:
        if failed:
            problems.append((priority, message))
    return [message for _, message in sorted(problems, reverse=True)[:3]]


def build_actions(student: dict[str, Any], risk_category: str) -> list[str]:
    actions: list[str] = []
    if _value(student, "attendance_percentage") < 75:
        actions.append("Create an attendance recovery plan and avoid non-essential absences for the next 30 days.")
    if _value(student, "assignment_completion_rate") < 70:
        actions.append("Use a weekly assignment tracker with two fixed submission review slots.")
    if _value(student, "subject_programming_score") < 60:
        actions.append("Practice programming for 45 minutes daily using small problem sets and lab exercises.")
    if _value(student, "subject_math_score") < 60:
        actions.append("Revise math fundamentals three times per week with solved examples.")
    if _value(student, "backlogs") > 0:
        actions.append("Break backlog preparation into topic-wise milestones and review progress with a mentor.")
    if _value(student, "stress_level") >= 7:
        actions.append("Schedule a mentor meeting to balance workload, deadlines, and recovery priorities.")
    if _value(student, "sleep_hours") < 6:
        actions.append("Set a consistent sleep routine and stop late-night study blocks during recovery.")

    risk_actions = {
        "Low Risk": [
            "Maintain current consistency and take one advanced mini-project.",
            "Use weekly self-review to keep GPA and attendance stable.",
        ],
        "Medium Risk": [
            "Follow a 14-day recovery plan focused on weak subjects and pending work.",
            "Check in with a mentor once per week until metrics stabilize.",
        ],
        "High Risk": [
            "Start immediate mentor intervention with a daily academic tracker.",
            "Prioritize attendance recovery, backlog planning, and assignment completion first.",
        ],
    }
    actions.extend(risk_actions.get(risk_category, risk_actions["Medium Risk"]))
    return actions[:5]


def generate_recommendations(student: dict[str, Any], risk_category: str = "Medium Risk") -> dict[str, Any]:
    top_problems = identify_top_problems(student)
    actions = build_actions(student, risk_category)

    if risk_category == "High Risk":
        summary = "Immediate academic support is recommended, with mentor-led recovery tracking."
        mentor_note = "Meet this student soon and agree on attendance, backlog, and assignment recovery milestones."
    elif risk_category == "Medium Risk":
        summary = "The student shows mixed signals and would benefit from a structured short-term improvement plan."
        mentor_note = "Review weak subjects and pending work weekly until the student returns to a stable pattern."
    else:
        summary = "The student is currently stable and should focus on consistency and advanced learning."
        mentor_note = "Encourage continued consistency and stretch learning through projects or peer mentoring."

    normalized_top_problems = top_problems or ["No major academic risk signals detected."]
    resources = [
        "College LMS lecture notes and quizzes",
        "Previous internal assessment papers",
        "Faculty office hours or mentor sessions",
        "Peer study group for difficult subjects",
    ]
    return {
        "student_id": student.get("student_id"),
        "risk_category": risk_category,
        "summary": summary,
        "top_problems": normalized_top_problems,
        "top_3_problems": normalized_top_problems,
        "action_plan": actions,
        "top_5_actions": actions,
        "seven_day_plan": [
            "Day 1: Review attendance, GPA, assignments, and weak subjects.",
            "Days 2-3: Clear the most urgent pending academic task.",
            "Days 4-5: Practice the weakest subject with targeted exercises.",
            "Day 6: Meet mentor or peer group for feedback.",
            "Day 7: Reflect, update tracker, and plan the next week.",
        ],
        "thirty_day_plan": [
            "Week 1: Stabilize attendance and pending submissions.",
            "Week 2: Focus on weak subject fundamentals.",
            "Week 3: Attempt practice tests and lab/problem-solving tasks.",
            "Week 4: Review progress with mentor and adjust the study plan.",
        ],
        "resources": resources,
        "mentor_note": mentor_note,
    }
