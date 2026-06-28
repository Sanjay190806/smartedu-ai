from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from dashboard import api_client
from dashboard.components.cards import render_empty_state, render_info_card, render_metric_card, status_badge
from dashboard.components.charts import risk_distribution_chart, weak_subjects_chart
from dashboard.components.layout import render_page_header, render_sidebar, render_workflow
from dashboard.components.tables import students_table
from dashboard.config import API_BASE_URL
from dashboard.utils.formatters import format_gpa, format_percentage


st.set_page_config(page_title="Executive Overview", layout="wide")
health = render_sidebar()
render_page_header(
    "Executive Overview",
    "Academic risk intelligence dashboard for early intervention and personalized student support.",
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
    render_metric_card("Total Students", data.get("total_students", 0), "Students visible to the platform", icon="Users")
with c2:
    render_metric_card("High Risk", data.get("high_risk_count", 0), "Immediate intervention queue", accent="#ef4444", icon="Alert")
with c3:
    render_metric_card("Medium Risk", data.get("medium_risk_count", 0), "Monitor and support", accent="#f59e0b", icon="Watch")
with c4:
    render_metric_card("Low Risk", data.get("low_risk_count", 0), "Stable academic pattern", accent="#22c55e", icon="Stable")

c5, c6, c7 = st.columns(3)
with c5:
    render_metric_card("Average Attendance", format_percentage(data.get("average_attendance")), "Class engagement signal", icon="Attend")
with c6:
    render_metric_card("Average GPA", format_gpa(data.get("average_gpa")), "Current academic performance", icon="GPA")
with c7:
    render_metric_card("Assignment Completion", format_percentage(data.get("average_assignment_completion")), "Submission consistency", icon="Tasks")

metrics_path = ROOT / "ml" / "model_registry" / "metrics.json"
if metrics_path.exists():
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    best_model = metrics.get("best_model", "-")
    best_metrics = metrics.get("models", {}).get(best_model, {})
    m1, m2, m3 = st.columns(3)
    with m1:
        render_metric_card("Selected Model", best_model, "Current trained classifier", icon="Model")
    with m2:
        render_metric_card("Macro F1", f"{best_metrics.get('f1_macro', 0):.3f}", "Balanced model quality", icon="F1")
    with m3:
        render_metric_card("High-Risk Recall", f"{best_metrics.get('high_risk_recall', 0):.3f}", "Intervention sensitivity", icon="Recall")

high_risk_count = int(data.get("high_risk_count", 0) or 0)
total_predictions = sum(int(data.get(key, 0) or 0) for key in ["low_risk_count", "medium_risk_count", "high_risk_count"])
if total_predictions == 0:
    render_empty_state(
        "Intervention insights locked",
        "Run predictions to unlock mentor priority insights and risk distribution analytics.",
        "Go to Risk Prediction or Batch Upload.",
    )
elif high_risk_count > 0:
    render_info_card(
        "Intervention Priority",
        f"Immediate mentor attention recommended for {high_risk_count} students.",
        icon="Priority",
    )
else:
    render_info_card("Intervention Priority", "No high-risk students detected yet.", icon="Clear")

left, right = st.columns(2)
with left:
    st.markdown("<div class='smart-card'><div class='section-title' style='margin-top:0'>Risk Distribution</div>", unsafe_allow_html=True)
    distribution = api_client.get_risk_distribution()
    if distribution.get("ok"):
        risk_distribution_chart(distribution["data"])
    else:
        st.warning(distribution.get("error"))
    st.markdown("</div>", unsafe_allow_html=True)
with right:
    st.markdown("<div class='smart-card'><div class='section-title' style='margin-top:0'>Weak Subject Insight</div>", unsafe_allow_html=True)
    weak_subjects_chart(data.get("top_weak_subjects", []))
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='section-title'>Recent Students</div>", unsafe_allow_html=True)
students = api_client.get_students()
if students.get("ok") and students.get("data"):
    students_table(students["data"][-10:])
else:
    render_empty_state(
        "No students yet",
        "Students are created automatically after running predictions or batch uploads.",
        "Go to Risk Prediction or Batch Upload.",
    )

render_workflow()
