from __future__ import annotations

import streamlit as st

from dashboard import api_client
from dashboard.config import API_BASE_URL, APP_SUBTITLE, APP_TITLE, DISCLAIMER
from dashboard.components.cards import render_command_card, status_badge
from dashboard.components.theme import THEME_OPTIONS, get_active_theme, inject_premium_css, set_active_theme


def render_page_header(title: str, subtitle: str | None = None) -> None:
    inject_premium_css()
    st.title(title)
    if subtitle:
        st.caption(subtitle)


def render_disclaimer() -> None:
    st.caption(DISCLAIMER)


def render_sidebar() -> dict:
    inject_premium_css()
    with st.sidebar:
        st.markdown("## SmartEdu AI")
        active = str(st.session_state.get("smartedu_theme", "dark")).title()
        selected = st.radio(
            "Theme",
            THEME_OPTIONS,
            index=THEME_OPTIONS.index(active) if active in THEME_OPTIONS else 0,
            horizontal=True,
        )
        set_active_theme(selected)
        inject_premium_css()
        st.caption(f"Active theme: {get_active_theme().title()}")
        st.divider()
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


def render_hero_section() -> None:
    inject_premium_css()
    st.markdown(
        f"""
        <div class="smart-hero">
          <div class="small-label">Academic AI Command Center</div>
          <h1>{APP_TITLE}</h1>
          <p><strong>{APP_SUBTITLE}</strong></p>
          <p>An academic risk intelligence dashboard that helps mentors identify struggling students early,
          understand why they are at risk, and generate personalized improvement plans.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_workflow() -> None:
    steps = ["Student Data", "Backend API", "ML Model", "Risk Score", "Explanation", "Recommendation", "Dashboard"]
    html = "<div class='smart-card'><div class='section-title' style='margin-top:0'>Workflow</div><div class='workflow'>"
    for index, step in enumerate(steps):
        html += f"<span class='workflow-step'>{step}</span>"
        if index < len(steps) - 1:
            html += "<span class='workflow-arrow'>-></span>"
    html += "</div></div>"
    st.markdown(html, unsafe_allow_html=True)


def render_footer_disclaimer() -> None:
    st.markdown(f"<div class='smart-card'><span class='small-label'>Ethical AI Note</span><p>{DISCLAIMER}</p></div>", unsafe_allow_html=True)


def render_command_grid() -> None:
    c1, c2, c3 = st.columns(3)
    with c1:
        render_command_card("Backend", "uvicorn backend.main:app --reload")
    with c2:
        render_command_card("Dashboard", "streamlit run dashboard/app.py")
    with c3:
        render_command_card("Tests", "python -m pytest")
