from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from dashboard import api_client
from dashboard.components.cards import risk_badge
from dashboard.components.forms import sample_payload_buttons, student_prediction_form
from dashboard.components.layout import render_page_header, render_sidebar
from dashboard.utils.formatters import format_probability
from dashboard.utils.validators import validate_student_payload


st.set_page_config(page_title="Risk Prediction", layout="wide")
render_sidebar()
render_page_header("Risk Prediction", "Run a single-student prediction through the FastAPI backend.")

sample_payload_buttons()
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
    st.subheader("Prediction Result")
    risk_badge(result["risk_category"])
    c1, c2 = st.columns(2)
    c1.metric("Probability", format_probability(result["probability"]))
    c2.metric("Confidence", result["confidence"])
    st.markdown("**Top factors**")
    for factor in result.get("top_factors", []):
        st.write(f"- {factor}")
    st.markdown("**Explanation**")
    st.write(result.get("explanation"))

    rec = result.get("recommendations", {})
    tab1, tab2, tab3 = st.tabs(["Actions", "Plans", "Resources"])
    with tab1:
        st.write(rec.get("summary"))
        st.markdown("**Top problems**")
        for item in rec.get("top_problems", []):
            st.write(f"- {item}")
        st.markdown("**Action plan**")
        for item in rec.get("action_plan", []):
            st.write(f"- {item}")
    with tab2:
        st.markdown("**7-day plan**")
        for item in rec.get("seven_day_plan", []):
            st.write(f"- {item}")
        st.markdown("**30-day plan**")
        for item in rec.get("thirty_day_plan", []):
            st.write(f"- {item}")
        st.markdown("**Mentor note**")
        st.info(rec.get("mentor_note", ""))
    with tab3:
        for item in rec.get("resources", []):
            st.write(f"- {item}")

    st.download_button(
        "Download prediction JSON",
        data=json.dumps(result, indent=2),
        file_name=f"{result.get('student_id', 'prediction')}_prediction.json",
        mime="application/json",
    )
