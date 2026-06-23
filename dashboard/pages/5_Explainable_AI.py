from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from dashboard import api_client
from dashboard.components.cards import risk_badge
from dashboard.components.charts import ranked_factors_chart
from dashboard.components.layout import render_page_header, render_sidebar
from dashboard.utils.formatters import format_probability


st.set_page_config(page_title="Explainable AI", layout="wide")
render_sidebar()
render_page_header("Explainable AI", "Explainable AI shows the main factors that influenced the risk prediction.")
st.caption("This helps mentors understand why the model made a prediction.")

students = api_client.get_students()
if not students.get("ok"):
    st.warning(students.get("error"))
    st.stop()
if not students.get("data"):
    st.info("No students found yet. Run a prediction first.")
    st.stop()

student_options = {f"{s['student_id']} - {s['name']}": s for s in students["data"]}
selected = st.selectbox("Select student", list(student_options.keys()))
student = student_options[selected]
record = student.get("latest_academic_record") or {}

if st.button("Run Prediction and Explanation", type="primary"):
    payload = {**{k: student[k] for k in ["student_id", "name", "department", "year", "semester", "gender"]}, **record}
    payload.pop("id", None)
    payload.pop("created_at", None)
    result = api_client.predict_student(payload)
    if not result.get("ok"):
        st.warning(result.get("error"))
        st.stop()
    data = result["data"]
    risk_badge(data["risk_category"])
    c1, c2 = st.columns(2)
    c1.metric("Probability", format_probability(data["probability"]))
    c2.metric("Confidence", data["confidence"])
    st.write(data.get("explanation"))
    st.subheader("Top Risk Factors")
    ranked_factors_chart(data.get("top_factors", []))
    st.subheader("Protective Factors")
    st.info("Protective factor details are not available yet. This can be added in future explainability upgrades.")
    st.warning("Explanation should support human decision-making, not replace mentor judgment.")
