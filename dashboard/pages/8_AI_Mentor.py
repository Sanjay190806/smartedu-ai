from __future__ import annotations

from pathlib import Path
import html
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from dashboard import api_client
from dashboard.components.cards import render_empty_state, render_metric_card, render_status_card
from dashboard.components.layout import render_page_header, render_sidebar
from dashboard.utils.report_export import mentor_report_to_markdown, mentor_report_to_text


st.set_page_config(page_title="AI Mentor", layout="wide")
render_sidebar()
render_page_header(
    "AI Mentor Intelligence",
    "Adaptive career interview, explainable guidance report, and offline-first AI provider fallback.",
)


def _set_session(data: dict) -> None:
    st.session_state["mentor_session"] = data
    st.session_state["mentor_report"] = None


def _refresh_session() -> None:
    session = st.session_state.get("mentor_session")
    if not session:
        return
    result = api_client.get_mentor_session(session["session_id"])
    if result.get("ok"):
        st.session_state["mentor_session"] = result["data"]


def _chips(values: list[str]) -> str:
    return "".join(f"<span class='smart-chip'>{html.escape(str(value))}</span>" for value in values)


def _card(title: str, body: str | None = None, label: str | None = None) -> None:
    st.markdown(
        f"""
        <div class="report-card">
          <div class="small-label">{html.escape(label or title)}</div>
          <h3>{html.escape(title)}</h3>
          <p class="muted-text">{html.escape(body or "Not available")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _list_card(title: str, items: list | dict | None) -> None:
    if isinstance(items, dict):
        rows = "".join(
            f"<div class='report-kv'><strong>{html.escape(str(key).replace('_', ' ').title())}</strong><span>{html.escape(', '.join(value) if isinstance(value, list) else str(value))}</span></div>"
            for key, value in items.items()
        )
        body = rows or "<p class='muted-text'>Not available</p>"
    else:
        rendered_items = []
        for item in items or []:
            if isinstance(item, dict):
                label = item.get("path") or item.get("career") or item.get("project_title") or item.get("title") or "Item"
                detail = item.get("why_it_may_fit") or item.get("why_it_fits") or item.get("reason") or item.get("risk_or_gap") or ""
                rendered_items.append(f"<li><strong>{html.escape(str(label))}</strong>{': ' + html.escape(str(detail)) if detail else ''}</li>")
            else:
                rendered_items.append(f"<li>{html.escape(str(item))}</li>")
        body = "<ul class='report-list'>" + "".join(rendered_items) + "</ul>"
    st.markdown(
        f"""
        <div class="report-card">
          <div class="small-label">{html.escape(title)}</div>
          {body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def _career_matrix(items: list[dict]) -> None:
    for item in items:
        score = int(item.get("match_score", 0))
        st.markdown(
            f"""
            <div class="report-card">
              <div class="small-label">Match Score {score}/100</div>
              <h3>{html.escape(str(item.get("career", "-")))}</h3>
              <p class="muted-text">{html.escape(str(item.get("why_it_fits", "-")))}</p>
              <p class="muted-text"><strong>Risk or gap:</strong> {html.escape(str(item.get("risk_or_gap", "-")))}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _project_cards(projects: list[dict]) -> None:
    for project in projects:
        st.markdown(
            f"""
            <div class="report-card">
              <div class="small-label">{html.escape(str(project.get("difficulty", "Project")))}</div>
              <h3>{html.escape(str(project.get("project_title", "-")))}</h3>
              <p class="muted-text">{html.escape(str(project.get("why_this_project", "-")))}</p>
              <p class="muted-text"><strong>Skills:</strong> {html.escape(", ".join(project.get("skills_used", [])))}</p>
              <p class="muted-text"><strong>Deliverables:</strong> {html.escape(", ".join(project.get("deliverables", [])))}</p>
              <p class="muted-text"><strong>GitHub value:</strong> {html.escape(str(project.get("github_value", "-")))}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


provider = api_client.get_mentor_provider_status()
provider_data = provider.get("data", {}) if provider.get("ok") else {}
top1, top2, top3, top4 = st.columns(4)
with top1:
    render_status_card("Mentor API", bool(provider.get("ok")), provider.get("error") or "Adaptive interview endpoints")
with top2:
    render_metric_card("Provider", provider_data.get("provider", "offline"), "Configured AI mode")
with top3:
    render_metric_card("Model", provider_data.get("active_model", "offline-rule-based"), "No API keys shown")
with top4:
    render_status_card("Fallback", provider_data.get("fallback_available", True), "Offline mentor engine available")

warning = provider_data.get("provider_warning")
if warning:
    st.info(warning)
elif provider_data.get("provider") == "offline":
    st.info("Offline mentor engine is active. Add OpenRouter or Groq API key in `.env` for deeper AI-generated reports.")
elif provider_data.get("provider") == "openrouter" and provider_data.get("real_ai_configured"):
    st.success("OpenRouter provider configured. API keys are not shown in the dashboard.")
elif provider_data.get("provider") == "groq" and provider_data.get("real_ai_configured"):
    st.success("Groq provider configured. API keys are not shown in the dashboard.")
st.caption("Configure AI providers in `.env`; never commit real API keys.")

st.markdown("<div class='section-title'>Start Interview</div>", unsafe_allow_html=True)
with st.form("mentor_start_form"):
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        student_id = st.text_input("Student ID", value="")
        department = st.selectbox("Department", ["Computer Science", "Electronics", "Information Technology", "Mechanical", "Civil", "Other"])
    with c2:
        student_name = st.text_input("Student Name", value="")
        year = st.number_input("Year", min_value=1, max_value=4, value=3)
    with c3:
        current_gpa = st.number_input("Current GPA", min_value=0.0, max_value=10.0, value=7.0, step=0.1)
        attendance = st.number_input("Attendance %", min_value=0.0, max_value=100.0, value=78.0, step=1.0)
    with c4:
        risk_category = st.selectbox("Risk Category", ["Unknown", "Low Risk", "Medium Risk", "High Risk"])
        max_questions = st.slider("Max Questions", min_value=8, max_value=20, value=15)
    submitted = st.form_submit_button("Start New Mentor Session")

if submitted:
    payload = {
        "student_id": student_id.strip() or None,
        "student_name": student_name.strip() or None,
        "max_questions": int(max_questions),
        "academic_context": {
            "department": department,
            "year": int(year),
            "current_gpa": float(current_gpa),
            "attendance_percentage": float(attendance),
            "risk_category": risk_category,
        },
    }
    result = api_client.start_mentor_session(payload)
    if result.get("ok"):
        _set_session(result["data"])
        st.success("Mentor session started.")
    else:
        st.error(result.get("error"))

_refresh_session()
session = st.session_state.get("mentor_session")

st.markdown("<div class='section-title'>Interview Workspace</div>", unsafe_allow_html=True)
if not session:
    render_empty_state("No active mentor session", "Start an interview above to generate adaptive career guidance.", "Offline mode works without external API keys.")
else:
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        render_metric_card("Session", session["session_id"], session.get("status", "active"))
    with s2:
        render_metric_card("Progress", f"{len(session.get('answers', []))}/{session.get('max_questions', 15)}", "Answered questions")
    with s3:
        render_metric_card("Clarity", f"{session.get('clarity_score', 0):.2f}", "Report readiness signal")
    with s4:
        render_metric_card("Direction", session.get("dominant_interest_area") or "Exploring", "Detected path signal")

    st.markdown(
        f"""
        <div class="mentor-note">
          <div class="small-label">Current Question</div>
          <h3>{session.get("current_question", "")}</h3>
          <p>{session.get("current_question_reason", "")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("mentor_answer_form", clear_on_submit=True):
        answer = st.text_area("Your answer", height=130, placeholder="Example: I enjoy Python, maths, and analyzing datasets. I want a practical project path.")
        send = st.form_submit_button("Submit Answer")
    if send:
        if not answer.strip():
            st.warning("Please write an answer before submitting.")
        else:
            response = api_client.submit_mentor_answer(session["session_id"], answer)
            if response.get("ok"):
                data = response["data"]
                if data.get("provider_warning"):
                    st.info(data["provider_warning"])
                st.session_state["mentor_last_analysis"] = data.get("previous_answer_analysis", {})
                _refresh_session()
                st.rerun()
            else:
                st.error(response.get("error"))

    analysis = st.session_state.get("mentor_last_analysis")
    if analysis:
        st.markdown("<div class='section-title'>Detected Signals</div>", unsafe_allow_html=True)
        a1, a2 = st.columns(2)
        with a1:
            st.markdown("<div class='smart-card'><div class='small-label'>Interests</div>" + _chips(analysis.get("detected_interests", [])) + "</div>", unsafe_allow_html=True)
        with a2:
            st.markdown("<div class='smart-card'><div class='small-label'>Possible Paths</div>" + _chips(analysis.get("possible_paths", [])) + "</div>", unsafe_allow_html=True)

    answers = session.get("answers", [])
    if answers:
        st.markdown("<div class='section-title'>Conversation Trace</div>", unsafe_allow_html=True)
        for item in answers[-5:]:
            st.markdown(
                f"""
                <div class="timeline-item">
                  <div class="small-label">Q{item.get("question_number")}: {item.get("question_text")}</div>
                  <p>{item.get("answer_text")}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    ready = session.get("status") in {"ready_for_report", "completed"} or len(answers) >= 8 or session.get("clarity_score", 0) >= 0.75
    c_report, c_load = st.columns([1, 1])
    with c_report:
        if st.button("Generate Mentor Report", disabled=not ready):
            report_result = api_client.generate_mentor_report(session["session_id"])
            if report_result.get("ok"):
                st.session_state["mentor_report"] = report_result["data"]
                st.success("Mentor report generated.")
                _refresh_session()
            else:
                st.error(report_result.get("error"))
    with c_load:
        if st.button("Load Saved Report"):
            saved = api_client.get_mentor_report(session["session_id"])
            if saved.get("ok"):
                st.session_state["mentor_report"] = saved["data"]
            else:
                st.warning(saved.get("error"))
    if not ready:
        st.caption("Answer at least 8 questions, reach clarity 0.75, or continue until max questions to unlock the final report.")

report_payload = st.session_state.get("mentor_report")
if report_payload:
    report = report_payload.get("report", {})
    st.markdown("<div class='section-title'>Mentor Report</div>", unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3)
    with r1:
        render_metric_card("Primary Path", report_payload.get("primary_career_path", "-"), "Career fit")
    with r2:
        render_metric_card("Confidence", f"{report_payload.get('confidence_score', 0):.2f}", "Based on interview clarity")
    with r3:
        render_metric_card("Report", report_payload.get("session_id", "-"), "Saved to backend")

    tabs = st.tabs(["Summary", "Career", "Skills", "Roadmap", "Projects", "Resources", "Mentor Advice", "Developer JSON"])
    with tabs[0]:
        executive = report.get("executive_summary", {})
        profile = report.get("student_profile_summary", {})
        risk = report.get("academic_risk_analysis", {})
        trace = report.get("career_reasoning_trace", {})
        _card("Executive Summary", executive.get("one_paragraph_summary", ""))
        p1, p2 = st.columns(2)
        with p1:
            _list_card("Student Profile", profile)
        with p2:
            _list_card("Readiness Scores", report.get("readiness_scores", {}))
        _list_card("Career Reasoning Trace", trace)
        _list_card("Academic Risk", risk)
    with tabs[1]:
        career = report.get("career_path_recommendation", {})
        _card(career.get("primary_path", "-"), career.get("why_this_path_fits", ""), label="Primary Path")
        c1, c2 = st.columns(2)
        with c1:
            _career_matrix(report.get("career_fit_matrix", []))
        with c2:
            _list_card("Secondary Paths", career.get("secondary_paths", []))
            _list_card("Paths To Avoid For Now", career.get("paths_to_avoid_for_now", []))
            _list_card("Confidence Breakdown", report.get("confidence_breakdown", {}))
    with tabs[2]:
        skill_gap = report.get("skill_gap_analysis", {})
        heatmap = report.get("skill_heatmap", {})
        s1, s2 = st.columns(2)
        with s1:
            _list_card("Current Skills", skill_gap.get("current_known_skills", []))
            _list_card("Missing Core Skills", skill_gap.get("missing_core_skills", []))
        with s2:
            _list_card("Skill Heatmap", heatmap)
            _list_card("SWOT Analysis", report.get("swot_analysis", {}))
    with tabs[3]:
        roadmap = report.get("personalized_skill_roadmap", {})
        daily = report.get("daily_learning_pattern", {})
        r_left, r_right = st.columns(2)
        with r_left:
            _list_card("30/60/90 Day Roadmap", roadmap)
            _list_card("One-Year Growth Plan", report.get("one_year_growth_plan", {}))
        with r_right:
            _list_card("Daily Learning Pattern", daily)
            _list_card("Weekly Plan", report.get("weekly_plan", {}))
    with tabs[4]:
        _project_cards(report.get("project_recommendations", []))
    with tabs[5]:
        resources = report.get("resource_recommendations", {})
        _list_card("Free Resources", resources.get("free_resources", []))
        _list_card("Practice Platforms", resources.get("practice_platforms", []))
        _list_card("Documentation To Read", resources.get("documentation_to_read", []))
        _list_card("Course Or YouTube Suggestions", resources.get("youtube_or_course_suggestions", []))
    with tabs[6]:
        advice = report.get("mentor_advice", {})
        _card("Short Advice", advice.get("short_advice", ""))
        _card("Hard Truth", advice.get("hard_truth", ""))
        _card("Encouragement", advice.get("encouragement", ""))
        _list_card("What To Stop Doing", advice.get("what_to_stop_doing", []))
        _list_card("What To Continue Doing", advice.get("what_to_continue_doing", []))
        _list_card("Mistake Warnings", report.get("mistake_warnings", []))
        _card("Parent Or Faculty Summary", report.get("parent_or_faculty_summary", ""))
        _list_card("Mentor Review Questions", report.get("mentor_review_questions", []))
    with tabs[7]:
        with st.expander("Developer JSON", expanded=False):
            st.json(report_payload)

    d1, d2, d3 = st.columns(3)
    with d1:
        st.download_button(
            "Download Report JSON",
            data=json.dumps(report_payload, indent=2),
            file_name=f"{report_payload.get('session_id', 'mentor')}_report.json",
            mime="application/json",
        )
    with d2:
        st.download_button(
            "Download Report Markdown",
            data=mentor_report_to_markdown(report_payload),
            file_name=f"{report_payload.get('session_id', 'mentor')}_report.md",
            mime="text/markdown",
        )
    with d3:
        st.download_button(
            "Download Report TXT",
            data=mentor_report_to_text(report_payload),
            file_name=f"{report_payload.get('session_id', 'mentor')}_report.txt",
            mime="text/plain",
        )

st.markdown("<div class='section-title'>Recent Mentor Sessions</div>", unsafe_allow_html=True)
sessions = api_client.list_mentor_sessions()
if sessions.get("ok") and sessions.get("data"):
    rows = [
        {
            "session_id": item.get("session_id"),
            "student_id": item.get("student_id"),
            "status": item.get("status"),
            "answers": len(item.get("answers", [])),
            "clarity_score": item.get("clarity_score"),
            "dominant_interest_area": item.get("dominant_interest_area"),
        }
        for item in sessions["data"]
    ]
    st.dataframe(rows, use_container_width=True, hide_index=True)
else:
    st.caption(sessions.get("error") or "No mentor sessions yet.")
