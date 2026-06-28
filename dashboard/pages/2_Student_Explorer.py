from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st

from dashboard import api_client
from dashboard.components.cards import render_empty_state, render_metric_card, render_risk_badge
from dashboard.components.charts import subject_performance_chart
from dashboard.components.layout import render_page_header, render_sidebar
from dashboard.config import API_BASE_URL
from dashboard.utils.formatters import format_datetime, format_gpa, format_percentage


st.set_page_config(page_title="Student Explorer", layout="wide")
render_sidebar()
render_page_header("Student Explorer", "Search students, inspect academic records, and run quick predictions.")

students_response = api_client.get_students()
if not students_response.get("ok"):
    st.warning(students_response.get("error"))
    st.stop()

students = students_response.get("data") or []
if not students:
    render_empty_state(
        "No students yet",
        "Students are created automatically after running predictions or batch uploads.",
        "Start with Risk Prediction or Batch Upload from the sidebar.",
    )
    cta1, cta2 = st.columns(2)
    cta1.info("Go to Risk Prediction to create one student profile.")
    cta2.info("Go to Batch Upload to create many student profiles.")
    st.stop()

df = pd.DataFrame(students)
st.markdown("<div class='smart-card'><div class='section-title' style='margin-top:0'>Filter Bar</div>", unsafe_allow_html=True)
filters = st.columns(4)
department = filters[0].selectbox("Department", ["All"] + sorted(df["department"].dropna().unique().tolist()))
year = filters[1].selectbox("Year", ["All"] + sorted(df["year"].dropna().unique().tolist()))
semester = filters[2].selectbox("Semester", ["All"] + sorted(df["semester"].dropna().unique().tolist()))
gender = filters[3].selectbox("Gender", ["All"] + sorted(df["gender"].dropna().unique().tolist()))
st.markdown("</div>", unsafe_allow_html=True)

filtered = df.copy()
if department != "All":
    filtered = filtered[filtered["department"] == department]
if year != "All":
    filtered = filtered[filtered["year"] == year]
if semester != "All":
    filtered = filtered[filtered["semester"] == semester]
if gender != "All":
    filtered = filtered[filtered["gender"] == gender]

if filtered.empty:
    render_empty_state("No students match these filters", "Adjust filters to expand the result set.")
    st.stop()

left, right = st.columns([1.05, 1.35])
with left:
    st.markdown("<div class='smart-card'><div class='section-title' style='margin-top:0'>Student List</div>", unsafe_allow_html=True)
    st.dataframe(
        filtered[["student_id", "name", "department", "year", "semester", "gender"]],
        use_container_width=True,
        hide_index=True,
    )
    selected_id = st.selectbox("Select student", filtered["student_id"].tolist())
    st.markdown("</div>", unsafe_allow_html=True)

student_response = api_client.get_student(selected_id)
if not student_response.get("ok"):
    st.warning(student_response.get("error"))
    st.stop()

student = student_response["data"]
record = student.get("latest_academic_record") or {}

with right:
    st.markdown("<div class='smart-card'><div class='section-title' style='margin-top:0'>Selected Student Profile</div>", unsafe_allow_html=True)
    st.subheader(student["name"])
    st.caption(
        f"{student['student_id']} | {student['department']} | Year {student['year']} | Semester {student['semester']} | {student['gender']}"
    )
    st.caption(f"Created: {format_datetime(student.get('created_at'))} | Updated: {format_datetime(student.get('updated_at'))}")
    p1, p2, p3 = st.columns(3)
    with p1:
        render_metric_card("Attendance", format_percentage(record.get("attendance_percentage")), "Presence and consistency")
    with p2:
        render_metric_card("Current GPA", format_gpa(record.get("current_gpa")), "Academic standing")
    with p3:
        render_metric_card("Assignments", format_percentage(record.get("assignment_completion_rate")), "Submission health")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-title'>Academic Snapshot</div>", unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
with m1:
    render_metric_card("Internal Marks", format_percentage(record.get("internal_marks_average")), "Assessment average")
with m2:
    render_metric_card("Quiz Average", format_percentage(record.get("quiz_average")), "Short assessment signal")
with m3:
    render_metric_card("Backlogs", record.get("backlogs", "-"), "Academic load risk", accent="#ef4444")
with m4:
    render_metric_card("Stress / Sleep", f"{record.get('stress_level', '-')}/{record.get('sleep_hours', '-')}", "Wellbeing context", accent="#f59e0b")

chart_col, action_col = st.columns([1.4, 1])
with chart_col:
    st.markdown("<div class='smart-card'><div class='section-title' style='margin-top:0'>Subject Performance</div>", unsafe_allow_html=True)
    subject_performance_chart(
        {
            "math": record.get("subject_math_score", 0),
            "programming": record.get("subject_programming_score", 0),
            "electronics": record.get("subject_electronics_score", 0),
            "communication": record.get("subject_communication_score", 0),
            "lab": record.get("subject_lab_score", 0),
        }
    )
    st.markdown("</div>", unsafe_allow_html=True)

with action_col:
    st.markdown("<div class='smart-card'><div class='section-title' style='margin-top:0'>Quick Actions</div>", unsafe_allow_html=True)
    payload = {**{k: student[k] for k in ["student_id", "name", "department", "year", "semester", "gender"]}, **record}
    payload.pop("id", None)
    payload.pop("created_at", None)
    if st.button("Predict Risk for Selected Student", use_container_width=True):
        result = api_client.predict_student(payload)
        if result.get("ok"):
            st.session_state.latest_prediction = result["data"]
            render_risk_badge(result["data"]["risk_category"])
            st.write(result["data"]["explanation"])
        else:
            st.warning(result.get("error"))
    if st.button("View Latest Recommendation", use_container_width=True):
        recommendation = api_client.get_recommendation(selected_id)
        if recommendation.get("ok"):
            st.session_state.selected_student_id = selected_id
            st.json(recommendation["data"], expanded=False)
        else:
            st.info("No recommendation found yet. Run a prediction first.")
    st.link_button("Open API Docs", f"{API_BASE_URL}/docs", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
