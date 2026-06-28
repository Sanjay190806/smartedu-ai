from __future__ import annotations

from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dashboard.components.cards import render_feature_card, render_status_card
from dashboard.components.layout import (
    render_command_grid,
    render_footer_disclaimer,
    render_hero_section,
    render_sidebar,
    render_workflow,
)
from dashboard.config import API_BASE_URL, APP_TITLE, PAGE_ICON
from dashboard.state import initialize_state


st.set_page_config(page_title=APP_TITLE, page_icon=PAGE_ICON, layout="wide")
initialize_state()
health = render_sidebar()

render_hero_section()

st.markdown("<div class='section-title'>System Readiness</div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
if health.get("ok"):
    data = health.get("data", {})
    with c1:
        render_status_card("Backend API", True, data.get("service", "SmartEdu AI Backend"))
    with c2:
        render_status_card("Model Artifacts", bool(data.get("model_loaded")), f"Loaded: {data.get('model_loaded')}")
    with c3:
        render_feature_card("API Docs", f"Open interactive FastAPI documentation at {API_BASE_URL}/docs", icon="Docs")
else:
    with c1:
        render_status_card("Backend API", False, "Start it with uvicorn backend.main:app --reload")
    with c2:
        render_feature_card("Offline Mode", "Dashboard pages render clean guidance even when the backend is unavailable.", icon="Safe")
    with c3:
        render_feature_card("Next Step", "Start the backend, then refresh this dashboard.", icon="Run")

st.markdown("<div class='section-title'>Product Capabilities</div>", unsafe_allow_html=True)
f1, f2, f3, f4 = st.columns(4)
with f1:
    render_feature_card("Risk Prediction", "Predict low, medium, or high academic risk from student performance data.", icon="AI")
with f2:
    render_feature_card("Explainable AI", "Show the top academic factors behind a prediction for mentor review.", icon="XAI")
with f3:
    render_feature_card("Personalized Guidance", "Generate 7-day and 30-day recovery plans with mentor notes.", icon="Plan")
with f4:
    render_feature_card("Batch Analytics", "Upload CSV files and analyze risk distribution across many students.", icon="CSV")

render_workflow()

st.markdown("<div class='section-title'>Quick Commands</div>", unsafe_allow_html=True)
render_command_grid()

st.markdown(f"[Open API docs]({API_BASE_URL}/docs)")
st.info("Use the sidebar to start with Risk Prediction or Batch Upload.")
render_footer_disclaimer()
