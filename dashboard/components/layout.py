from __future__ import annotations

import streamlit as st

from dashboard import api_client
from dashboard.config import API_BASE_URL, DISCLAIMER
from dashboard.components.cards import status_badge


def render_page_header(title: str, subtitle: str | None = None) -> None:
    st.title(title)
    if subtitle:
        st.caption(subtitle)


def render_disclaimer() -> None:
    st.caption(DISCLAIMER)


def render_sidebar() -> dict:
    with st.sidebar:
        st.markdown("## SmartEdu AI")
        health = api_client.check_backend_health()
        status_badge("Backend", bool(health.get("ok")))
        if health.get("ok"):
            data = health.get("data", {})
            st.caption(f"Service: {data.get('service', 'SmartEdu AI Backend')}")
            st.caption(f"Model loaded: {data.get('model_loaded')}")
        else:
            st.warning(health.get("error"))
            st.code("uvicorn backend.main:app --reload")
        st.markdown(f"[API docs]({API_BASE_URL}/docs)")
        st.divider()
        render_disclaimer()
    return health
