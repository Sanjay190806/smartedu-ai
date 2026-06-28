from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from dashboard import api_client
from dashboard.components.cards import render_empty_state, render_info_card, render_metric_card, render_risk_badge
from dashboard.components.charts import ranked_factors_chart
from dashboard.components.layout import render_page_header, render_sidebar
from dashboard.utils.formatters import format_probability


st.set_page_config(page_title="Explainable AI", layout="wide")
render_sidebar()
render_page_header("Explainable AI", "Understand the academic factors behind each risk prediction.")

render_info_card(
    "Why did the model predict this?",
    "Explainability helps mentors see why a model predicted a risk level, so intervention can focus on the most useful academic and wellbeing signals.",
    icon="XAI",
)

students = api_client.get_students()
if not students.get("ok"):
    st.warning(students.get("error"))
    st.stop()
if not students.get("data"):
    render_empty_state("No students yet", "Run a prediction first, then return here for factor explanations.")
    st.stop()

st.markdown("<div class='smart-card'><div class='section-title' style='margin-top:0'>Student Selection</div>", unsafe_allow_html=True)
student_options = {f"{s['student_id']} - {s['name']}": s for s in students["data"]}
selected = st.selectbox("Select student", list(student_options.keys()))
student = student_options[selected]
record = student.get("latest_academic_record") or {}
run = st.button("Run Prediction and Explanation", type="primary", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

if run:
    payload = {**{k: student[k] for k in ["student_id", "name", "department", "year", "semester", "gender"]}, **record}
    payload.pop("id", None)
    payload.pop("created_at", None)
    result = api_client.predict_student(payload)
    if not result.get("ok"):
        st.warning(result.get("error"))
        st.stop()
    data = result["data"]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='smart-card'><div class='small-label'>Risk Category</div>", unsafe_allow_html=True)
        render_risk_badge(data["risk_category"])
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        render_metric_card("Probability", format_probability(data["probability"]), "Predicted class probability")
    with c3:
        render_metric_card("Confidence", data["confidence"], "Confidence band")

    render_info_card("Student-Friendly Explanation", data.get("explanation", ""), icon="Narrative")

    factor_cols = st.columns(2)
    with factor_cols[0]:
        st.markdown("<div class='smart-card'><div class='section-title' style='margin-top:0'>Ranked Risk Factors</div>", unsafe_allow_html=True)
        ranked_factors_chart(data.get("top_factors", []))
        st.markdown("</div>", unsafe_allow_html=True)
    with factor_cols[1]:
        st.markdown("<div class='smart-card'><div class='section-title' style='margin-top:0'>Factor Cards</div>", unsafe_allow_html=True)
        for index, factor in enumerate(data.get("top_factors", []), start=1):
            st.markdown(f"<div class='insight-card'><strong>{index}.</strong> {factor}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    render_info_card(
        "Future Explainability Upgrade",
        "Protective factors and SHAP waterfall charts can be added in a future explainability upgrade.",
        icon="Planned",
    )
    st.warning("Explanation should support human decision-making, not replace mentor judgment.")
