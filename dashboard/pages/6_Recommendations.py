from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from dashboard import api_client
from dashboard.components.cards import render_empty_state, render_info_card, render_risk_badge
from dashboard.components.layout import render_page_header, render_sidebar


st.set_page_config(page_title="Recommendations", layout="wide")
render_sidebar()
render_page_header("Recommendations", "Personalized academic improvement plans generated from risk signals.")

students = api_client.get_students()
if not students.get("ok"):
    st.warning(students.get("error"))
    st.stop()
if not students.get("data"):
    render_empty_state("No students yet", "Run a prediction first to create a recommendation-ready student profile.")
    st.stop()

st.markdown("<div class='smart-card'><div class='section-title' style='margin-top:0'>Student Selector</div>", unsafe_allow_html=True)
student_options = {f"{s['student_id']} - {s['name']}": s for s in students["data"]}
selected = st.selectbox("Select student", list(student_options.keys()))
student = student_options[selected]
student_id = student["student_id"]
st.markdown("</div>", unsafe_allow_html=True)

recommendation = api_client.get_recommendation(student_id)
if not recommendation.get("ok"):
    render_empty_state(
        "No recommendation found",
        "Run a prediction for this student to generate a personalized academic plan.",
        "Use the button below or go to Risk Prediction.",
    )
    if st.button("Generate from Latest Academic Record", use_container_width=True):
        record = student.get("latest_academic_record") or {}
        payload = {**{k: student[k] for k in ["student_id", "name", "department", "year", "semester", "gender"]}, **record}
        payload.pop("id", None)
        payload.pop("created_at", None)
        result = api_client.predict_student(payload)
        if result.get("ok"):
            recommendation = {"ok": True, "data": result["data"]["recommendations"]}
        else:
            st.warning(result.get("error"))
            st.stop()

if recommendation.get("ok"):
    rec = recommendation["data"]
    top_left, top_right = st.columns([1, 2])
    with top_left:
        st.markdown("<div class='smart-card'><div class='small-label'>Risk Category</div>", unsafe_allow_html=True)
        render_risk_badge(rec.get("risk_category", "Medium Risk"))
        st.markdown("</div>", unsafe_allow_html=True)
    with top_right:
        render_info_card("Guidance Summary", rec.get("summary", ""), icon="Mentor")

    tab1, tab2, tab3, tab4 = st.tabs(["Problems", "Action Plan", "Roadmap", "Mentor Copy"])
    with tab1:
        for item in rec.get("top_problems", []):
            st.markdown(f"<div class='insight-card'><strong>Concern</strong><br>{item}</div>", unsafe_allow_html=True)
    with tab2:
        for item in rec.get("action_plan", []):
            st.checkbox(item, value=False)
    with tab3:
        st.markdown("**7-day recovery timeline**")
        for item in rec.get("seven_day_plan", []):
            st.markdown(f"<div class='timeline-item'>{item}</div>", unsafe_allow_html=True)
        st.markdown("**30-day weekly roadmap**")
        for item in rec.get("thirty_day_plan", []):
            st.markdown(f"<div class='timeline-item'>{item}</div>", unsafe_allow_html=True)
        st.markdown("**Resources**")
        for item in rec.get("resources", []):
            st.markdown(f"<span class='smart-chip'>{item}</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='mentor-note'><strong>Mentor note</strong><br>{rec.get('mentor_note', '')}</div>", unsafe_allow_html=True)
    with tab4:
        mentor_text = (
            f"Student: {student.get('name')} ({student_id})\n"
            f"Risk: {rec.get('risk_category')}\n\n"
            f"Main concerns:\n" + "\n".join(f"- {item}" for item in rec.get("top_problems", [])) + "\n\n"
            f"Next 7 days:\n" + "\n".join(f"- {item}" for item in rec.get("seven_day_plan", [])) + "\n\n"
            f"Mentor note:\n{rec.get('mentor_note', '')}"
        )
        st.text_area("Copy-ready mentor summary", mentor_text, height=280)
        d1, d2 = st.columns(2)
        d1.download_button("Download Text", mentor_text, f"{student_id}_recommendation.txt", "text/plain", use_container_width=True)
        d2.download_button("Download JSON", json.dumps(rec, indent=2), f"{student_id}_recommendation.json", "application/json", use_container_width=True)
