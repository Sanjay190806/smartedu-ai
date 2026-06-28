from __future__ import annotations

from typing import Any


def _lines_from_list(items: list[Any]) -> list[str]:
    lines = []
    for item in items:
        if isinstance(item, dict):
            label = item.get("project_title") or item.get("career") or item.get("path") or item.get("skill") or "Item"
            details = item.get("why_this_project") or item.get("why_it_fits") or item.get("why_it_may_fit") or item.get("reason") or ""
            lines.append(f"- **{label}**: {details}" if details else f"- {label}")
        else:
            lines.append(f"- {item}")
    return lines


def _section(title: str, body: str | list[str]) -> list[str]:
    lines = [f"## {title}", ""]
    if isinstance(body, list):
        lines.extend(body or ["- Not available"])
    else:
        lines.append(body or "Not available")
    lines.append("")
    return lines


def mentor_report_to_markdown(report_payload: dict[str, Any]) -> str:
    report = report_payload.get("report", report_payload)
    executive = report.get("executive_summary", {})
    career = report.get("career_path_recommendation", {})
    skills = report.get("skill_gap_analysis", {})
    roadmap = report.get("personalized_skill_roadmap", {})
    weekly = report.get("weekly_plan", {})
    projects = report.get("project_recommendations", [])
    advice = report.get("mentor_advice", {})

    lines = ["# SmartEdu AI Mentor Report", ""]
    lines.extend(_section("Executive Summary", executive.get("one_paragraph_summary", "")))
    lines.extend(_section("Career Recommendation", [
        f"- **Primary path:** {career.get('primary_path', report_payload.get('primary_career_path', '-'))}",
        f"- **Why it fits:** {career.get('why_this_path_fits', '-')}",
    ]))
    lines.extend(_section("Skill Roadmap", [
        f"- **Known skills:** {', '.join(skills.get('current_known_skills', [])) or '-'}",
        f"- **Build first:** {', '.join(skills.get('skills_to_improve_first', [])) or '-'}",
        f"- **Next 30 days:** {', '.join(roadmap.get('next_30_days', [])) or '-'}",
        f"- **Next 90 days:** {', '.join(roadmap.get('next_90_days', [])) or '-'}",
    ]))
    weekly_lines = [f"- **{day.title()}:** {', '.join(tasks)}" for day, tasks in weekly.items()]
    lines.extend(_section("Weekly Plan", weekly_lines))
    lines.extend(_section("Projects", _lines_from_list(projects)))
    lines.extend(_section("Mentor Advice", [
        f"- **Advice:** {advice.get('short_advice', '-')}",
        f"- **Hard truth:** {advice.get('hard_truth', '-')}",
        f"- **Next action:** {advice.get('next_best_action', '-')}",
    ]))
    return "\n".join(lines).strip() + "\n"


def mentor_report_to_text(report_payload: dict[str, Any]) -> str:
    markdown = mentor_report_to_markdown(report_payload)
    return (
        markdown.replace("# ", "")
        .replace("## ", "")
        .replace("**", "")
        .replace("- ", "  - ")
    )
