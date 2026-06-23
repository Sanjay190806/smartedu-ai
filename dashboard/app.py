from __future__ import annotations

from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dashboard.components.layout import render_sidebar
from dashboard.config import API_BASE_URL, APP_SUBTITLE, APP_TITLE, PAGE_ICON
from dashboard.state import initialize_state


st.set_page_config(page_title=APP_TITLE, page_icon=PAGE_ICON, layout="wide")
initialize_state()
health = render_sidebar()

st.title(APP_TITLE)
st.caption(APP_SUBTITLE)
st.markdown(
    "A dashboard for academic risk intelligence, explainable predictions, and personalized student support."
)

if not health.get("ok"):
    st.warning("Backend is not running. Start it with: uvicorn backend.main:app --reload")
    st.code("uvicorn backend.main:app --reload")
else:
    st.success("Backend is online and ready.")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Backend**")
    st.code("uvicorn backend.main:app --reload")
with col2:
    st.markdown("**Dashboard**")
    st.code("streamlit run dashboard/app.py")

st.markdown(f"[Open API docs]({API_BASE_URL}/docs)")
st.info("Use the pages in the sidebar to explore analytics, predictions, batch upload, explainability, recommendations, and system status.")
