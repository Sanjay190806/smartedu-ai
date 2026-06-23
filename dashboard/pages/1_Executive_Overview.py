from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from dashboard import api_client
from dashboard.components.cards import metric_card, status_badge
from dashboard.components.charts import risk_distribution_chart, weak_subjects_chart
from dashboard.components.layout import render_page_header, render_sidebar
from dashboard.components.tables import students_table
from dashboard.config import API_BASE_URL
from dashboard.utils.formatters import format_gpa, format_percentage


st.set_page_config(page_title="Executive Overview", layout="wide")
health = render_sidebar()
render_page_header(
    "SmartEdu AI Executive Overview",
    "Academic risk intelligence dashboard for early intervention and personalized guidance.",
)

status_badge("Backend", bool(health.get("ok")))
if health.get("ok"):
    st.caption(f"Model loaded: {health.get('data', {}).get('model_loaded')}")
st.markdown(f"[API docs]({API_BASE_URL}/docs)")

summary = api_client.get_analytics_summary()
if not summary.get("ok"):
    st.warning(summary.get("error"))
    st.stop()

data = summary["data"]
c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card("Total students", data.get("total_students", 0))
with c2:
    metric_card("Low risk", data.get("low_risk_count", 0))
with c3:
    metric_card("Medium risk", data.get("medium_risk_count", 0))
with c4:
    metric_card("High risk", data.get("high_risk_count", 0))

c5, c6, c7 = st.columns(3)
with c5:
    metric_card("Average attendance", format_percentage(data.get("average_attendance")))
with c6:
    metric_card("Average GPA", format_gpa(data.get("average_gpa")))
with c7:
    metric_card("Assignment completion", format_percentage(data.get("average_assignment_completion")))

left, right = st.columns(2)
with left:
    st.subheader("Risk Distribution")
    distribution = api_client.get_risk_distribution()
    if distribution.get("ok"):
        risk_distribution_chart(distribution["data"])
    else:
        st.warning(distribution.get("error"))
with right:
    st.subheader("Weak Subject Insight")
    weak_subjects_chart(data.get("top_weak_subjects", []))

st.subheader("Recent Students")
students = api_client.get_students()
if students.get("ok") and students.get("data"):
    students_table(students["data"][-10:])
else:
    st.info("No saved students found yet. Run a prediction or upload a batch CSV.")

st.subheader("Project Workflow")
st.markdown("Student Data -> FastAPI Backend -> ML Model -> Risk Prediction -> Explanation -> Recommendations -> Dashboard")
