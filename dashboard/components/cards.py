from __future__ import annotations

import html

import streamlit as st

from dashboard.utils.formatters import risk_label_to_color


def metric_card(label: str, value, help_text: str | None = None) -> None:
    st.metric(label, value, help=help_text)


def risk_badge(risk: str) -> None:
    color = risk_label_to_color(risk)
    st.markdown(
        f"<span style='display:inline-block;padding:0.35rem 0.65rem;border-radius:0.5rem;"
        f"background:{color};color:white;font-weight:700'>{html.escape(risk)}</span>",
        unsafe_allow_html=True,
    )


def status_badge(label: str, online: bool) -> None:
    color = "#15803d" if online else "#b91c1c"
    text = "Online" if online else "Offline"
    st.markdown(
        f"<span style='display:inline-block;padding:0.3rem 0.6rem;border-radius:0.45rem;"
        f"background:{color};color:white;font-weight:700'>{html.escape(label)}: {text}</span>",
        unsafe_allow_html=True,
    )


def info_card(title: str, body: str) -> None:
    st.markdown(f"**{title}**")
    st.write(body)
