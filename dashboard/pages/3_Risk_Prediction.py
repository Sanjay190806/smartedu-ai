from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from dashboard import api_client
from dashboard.components.cards import render_info_card, render_metric_card, render_risk_badge
from dashboard.components.forms import sample_payload_buttons, student_prediction_form
from dashboard.components.layout import render_page_header, render_sidebar
from dashboard.utils.formatters import format_probability
from dashboard.utils.validators import validate_student_payload


st.set_page_config(page_title="Risk Prediction", layout="wide")
render_sidebar()
render_page_header("Risk Prediction", "Run a single-student prediction through the SmartEdu AI backend.")

st.markdown("<div class='section-title'>Demo Profiles</div>", unsafe_allow_html=True)
sample_payload_buttons()

st.markdown("<div class='section-title'>Prediction Workspace</div>", unsafe_allow_html=True)
form = student_prediction_form()

if form["submitted"]:
    valid, errors = validate_student_payload(form["payload"])
    if not valid:
        st.error("; ".join(errors))
        st.stop()
    response = api_client.predict_student(form["payload"])
    if not response.get("ok"):
        st.warning(response.get("error"))
        st.stop()

    result = response["data"]
    st.session_state.latest_prediction = result
    rec = result.get("recommendations", {})

    st.markdown("<div class='section-title'>Prediction Result</div>", unsafe_allow_html=True)
    top, mid, right = st.columns([1, 1, 1])
    with top:
        st.markdown("<div class='smart-card'><div class='small-label'>Risk Category</div>", unsafe_allow_html=True)
        render_risk_badge(result["risk_category"])
        st.markdown("</div>", unsafe_allow_html=True)
    with mid:
        render_metric_card("Probability", format_probability(result["probability"]), "Predicted class probability", icon="Score")
    with right:
        render_metric_card("Confidence", result["confidence"], "Model confidence band", icon="Signal")

    render_info_card("Why this prediction?", result.get("explanation", ""), icon="Explanation")

    factor_cols = st.columns(3)
    for index, factor in enumerate(result.get("top_factors", [])[:6]):
        with factor_cols[index % 3]:
            render_info_card(f"Factor {index + 1}", factor, icon="Risk")

    st.markdown("<div class='section-title'>Recommendation Plan</div>", unsafe_allow_html=True)
    render_info_card("Summary", rec.get("summary", ""), icon="Plan")
    tab1, tab2, tab3 = st.tabs(["Action Plan", "Recovery Roadmap", "Resources"])
    with tab1:
        st.markdown("**Top problems**")
        for item in rec.get("top_problems", []):
            st.markdown(f"<div class='insight-card'>{item}</div>", unsafe_allow_html=True)
        st.markdown("**Action checklist**")
        for item in rec.get("action_plan", []):
            st.checkbox(item, value=False)
    with tab2:
        st.markdown("**7-day plan**")
        for item in rec.get("seven_day_plan", []):
            st.markdown(f"<div class='timeline-item'>{item}</div>", unsafe_allow_html=True)
        st.markdown("**30-day roadmap**")
        for item in rec.get("thirty_day_plan", []):
            st.markdown(f"<div class='timeline-item'>{item}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='mentor-note'><strong>Mentor note</strong><br>{rec.get('mentor_note', '')}</div>", unsafe_allow_html=True)
    with tab3:
        for item in rec.get("resources", []):
            st.markdown(f"<span class='smart-chip'>{item}</span>", unsafe_allow_html=True)

    mentor_summary = (
        f"Student: {result.get('student_id')}\n"
        f"Risk: {result.get('risk_category')}\n"
        f"Main concerns:\n" + "\n".join(f"- {item}" for item in rec.get("top_problems", [])) + "\n\n"
        f"Next 7 days:\n" + "\n".join(f"- {item}" for item in rec.get("seven_day_plan", [])) + "\n\n"
        f"Mentor note:\n{rec.get('mentor_note', '')}"
    )
    d1, d2 = st.columns(2)
    d1.download_button(
        "Download JSON Report",
        data=json.dumps(result, indent=2),
        file_name=f"{result.get('student_id', 'prediction')}_prediction.json",
        mime="application/json",
        use_container_width=True,
    )
    d2.download_button(
        "Download Mentor Summary",
        data=mentor_summary,
        file_name=f"{result.get('student_id', 'prediction')}_mentor_summary.txt",
        mime="text/plain",
        use_container_width=True,
    )
