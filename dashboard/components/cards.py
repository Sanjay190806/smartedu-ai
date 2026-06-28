from __future__ import annotations

import html

import streamlit as st

from dashboard.utils.formatters import risk_label_to_color


def metric_card(label: str, value, help_text: str | None = None) -> None:
    st.metric(label, value, help=help_text)


def render_metric_card(
    title: str,
    value,
    subtitle: str | None = None,
    accent: str | None = None,
    icon: str | None = None,
) -> None:
    border_color = accent or "#60a5fa"
    st.markdown(
        f"""
        <div class="metric-card" style="--blue:{html.escape(border_color)}">
          <div class="metric-label">{html.escape(icon + " " if icon else "")}{html.escape(title)}</div>
          <div class="metric-value">{html.escape(str(value))}</div>
          <div class="metric-subtitle">{html.escape(subtitle or "")}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_status_card(title: str, status: bool | str, description: str | None = None) -> None:
    online = status is True or str(status).lower() in {"ok", "online", "true"}
    css_class = "status-online" if online else "status-offline"
    label = "Online" if online else "Offline"
    st.markdown(
        f"""
        <div class="smart-card">
          <div class="small-label">{html.escape(title)}</div>
          <div style="margin-top:.65rem"><span class="status-badge {css_class}">{label}</span></div>
          <p style="color:#aab8cb;margin-bottom:0">{html.escape(description or "")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def risk_badge(risk: str) -> None:
    render_risk_badge(risk)


def render_risk_badge(risk_category: str) -> None:
    risk = risk_category or "Unknown"
    css_class = {
        "Low Risk": "risk-low",
        "Medium Risk": "risk-medium",
        "High Risk": "risk-high",
    }.get(risk, "risk-medium")
    st.markdown(
        f"<span class='risk-badge {css_class}'>{html.escape(risk)}</span>",
        unsafe_allow_html=True,
    )


def status_badge(label: str, online: bool) -> None:
    css_class = "status-online" if online else "status-offline"
    text = "Online" if online else "Offline"
    st.markdown(
        f"<span class='status-badge {css_class}'>{html.escape(label)}: {text}</span>",
        unsafe_allow_html=True,
    )


def info_card(title: str, body: str) -> None:
    render_info_card(title, body)


def render_info_card(title: str, body: str, icon: str | None = None) -> None:
    st.markdown(
        f"""
        <div class="smart-card">
          <div class="section-title" style="margin-top:0">{html.escape(icon + " " if icon else "")}{html.escape(title)}</div>
          <p style="color:#cbd5e1;margin-bottom:0">{html.escape(body)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(title: str, message: str, action_text: str | None = None) -> None:
    st.markdown(
        f"""
        <div class="empty-state">
          <h3>{html.escape(title)}</h3>
          <p style="color:#aab8cb">{html.escape(message)}</p>
          <div class="small-label">{html.escape(action_text or "")}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_card(title: str, description: str, icon: str | None = None) -> None:
    render_info_card(title, description, icon=icon)


def render_command_card(title: str, command: str) -> None:
    st.markdown(f"**{title}**")
    st.markdown(
        f"<div class='command-box'><div class='small-label'>{html.escape(title)}</div><code>{html.escape(command)}</code></div>",
        unsafe_allow_html=True,
    )
