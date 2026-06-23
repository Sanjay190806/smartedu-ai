from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st

from dashboard import api_client
from dashboard.components.cards import risk_badge
from dashboard.components.charts import subject_performance_chart
from dashboard.components.layout import render_page_header, render_sidebar
from dashboard.components.messages import empty_state
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
    empty_state("No students found yet. Run a prediction or batch upload first.")
    st.stop()

df = pd.DataFrame(students)
filters = st.columns(4)
department = filters[0].selectbox("Department", ["All"] + sorted(df["department"].dropna().unique().tolist()))
year = filters[1].selectbox("Year", ["All"] + sorted(df["year"].dropna().unique().tolist()))
semester = filters[2].selectbox("Semester", ["All"] + sorted(df["semester"].dropna().unique().tolist()))
gender = filters[3].selectbox("Gender", ["All"] + sorted(df["gender"].dropna().unique().tolist()))

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
    empty_state("No students match the selected filters.")
    st.stop()

selected_id = st.selectbox("Select student", filtered["student_id"].tolist())
student_response = api_client.get_student(selected_id)
if not student_response.get("ok"):
    st.warning(student_response.get("error"))
    st.stop()

student = student_response["data"]
record = student.get("latest_academic_record") or {}
st.subheader(student["name"])
c1, c2, c3, c4 = st.columns(4)
c1.metric("Student ID", student["student_id"])
c2.metric("Department", student["department"])
c3.metric("Year", student["year"])
c4.metric("Semester", student["semester"])
st.caption(f"Gender: {student['gender']} | Created: {format_datetime(student.get('created_at'))} | Updated: {format_datetime(student.get('updated_at'))}")

st.subheader("Latest Academic Record")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Attendance", format_percentage(record.get("attendance_percentage")))
m2.metric("Current GPA", format_gpa(record.get("current_gpa")))
m3.metric("Internal Marks", format_percentage(record.get("internal_marks_average")))
m4.metric("Assignments", format_percentage(record.get("assignment_completion_rate")))
m5, m6, m7, m8 = st.columns(4)
m5.metric("Quiz Average", format_percentage(record.get("quiz_average")))
m6.metric("Backlogs", record.get("backlogs", "-"))
m7.metric("Stress Level", record.get("stress_level", "-"))
m8.metric("Sleep Hours", record.get("sleep_hours", "-"))

subjects = {
    "math": record.get("subject_math_score", 0),
    "programming": record.get("subject_programming_score", 0),
    "electronics": record.get("subject_electronics_score", 0),
    "communication": record.get("subject_communication_score", 0),
    "lab": record.get("subject_lab_score", 0),
}
subject_performance_chart(subjects)

c9, c10, c11 = st.columns(3)
if c9.button("Predict Risk for Selected Student", use_container_width=True):
    payload = {**{k: student[k] for k in ["student_id", "name", "department", "year", "semester", "gender"]}, **record}
    payload.pop("id", None)
    payload.pop("created_at", None)
    result = api_client.predict_student(payload)
    if result.get("ok"):
        st.session_state.latest_prediction = result["data"]
        risk_badge(result["data"]["risk_category"])
        st.write(result["data"]["explanation"])
    else:
        st.warning(result.get("error"))
if c10.button("View Recommendation", use_container_width=True):
    recommendation = api_client.get_recommendation(selected_id)
    if recommendation.get("ok"):
        st.json(recommendation["data"], expanded=False)
    else:
        st.info("No recommendation found yet. Run a prediction first.")
c11.link_button("Open API Docs", f"{API_BASE_URL}/docs", use_container_width=True)
