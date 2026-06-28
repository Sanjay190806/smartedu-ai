from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from dashboard.components.theme import get_active_theme, get_plotly_template, get_risk_colors


def _apply_theme_layout(fig):
    theme = get_active_theme()
    font_color = "#102033" if theme == "light" else "#dbeafe"
    fig.update_layout(
        template=get_plotly_template(theme),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": font_color},
        margin={"l": 20, "r": 20, "t": 40, "b": 30},
    )
    return fig


def risk_distribution_chart(distribution: dict[str, int], chart_type: str = "bar") -> None:
    df = pd.DataFrame(
        [{"risk": risk, "count": int(count)} for risk, count in distribution.items()]
    )
    if df.empty or df["count"].sum() == 0:
        st.info("No prediction records found yet. Run a prediction or upload a batch CSV.")
        return
    if chart_type == "pie":
        fig = px.pie(df, values="count", names="risk", hole=0.45, color="risk", color_discrete_map=get_risk_colors())
    else:
        fig = px.bar(df, x="risk", y="count", color="risk", color_discrete_map=get_risk_colors(), text="count")
        fig.update_layout(xaxis_title="", yaxis_title="Students")
    _apply_theme_layout(fig)
    st.plotly_chart(fig, use_container_width=True)


def subject_performance_chart(subjects: dict[str, float]) -> None:
    df = pd.DataFrame([{"subject": key.title(), "score": value} for key, value in subjects.items()])
    theme = get_active_theme()
    sequence = ["#0f7ea8", "#2563eb", "#7c3aed", "#b45309", "#15803d"] if theme == "light" else ["#22d3ee", "#60a5fa", "#a78bfa", "#f59e0b", "#22c55e"]
    fig = px.bar(df, x="subject", y="score", text="score", color="subject", color_discrete_sequence=sequence)
    fig.update_layout(showlegend=False, yaxis_range=[0, 100], xaxis_title="", yaxis_title="Average score")
    _apply_theme_layout(fig)
    st.plotly_chart(fig, use_container_width=True)


def weak_subjects_chart(subjects: list[str]) -> None:
    if not subjects:
        st.info("Weak subject insight is not available yet.")
        return
    df = pd.DataFrame({"subject": [subject.title() for subject in subjects], "rank": list(range(1, len(subjects) + 1))})
    fig = px.bar(df, x="rank", y="subject", orientation="h", text="subject", color="subject")
    fig.update_layout(showlegend=False, xaxis_title="Priority rank", yaxis_title="")
    _apply_theme_layout(fig)
    st.plotly_chart(fig, use_container_width=True)


def attendance_gpa_scatter(df: pd.DataFrame) -> None:
    if df.empty or not {"attendance_percentage", "current_gpa"}.issubset(df.columns):
        st.info("Attendance vs GPA data is not available.")
        return
    fig = px.scatter(df, x="attendance_percentage", y="current_gpa", hover_data=["student_id", "name"])
    fig.update_layout(xaxis_title="Attendance %", yaxis_title="Current GPA")
    _apply_theme_layout(fig)
    st.plotly_chart(fig, use_container_width=True)


def ranked_factors_chart(factors: list[str]) -> None:
    if not factors:
        st.info("No top factors returned for this prediction.")
        return
    fig = go.Figure(go.Bar(x=list(range(len(factors), 0, -1)), y=factors, orientation="h"))
    fig.update_layout(xaxis_title="Relative rank", yaxis_title="", height=max(260, 50 * len(factors)))
    _apply_theme_layout(fig)
    st.plotly_chart(fig, use_container_width=True)


def model_metrics_chart(metrics: dict[str, float]) -> None:
    if not metrics:
        st.info("Model metrics are not available yet.")
        return
    df = pd.DataFrame(
        [{"metric": key.replace("_", " ").title(), "value": float(value)} for key, value in metrics.items()]
    )
    fig = px.bar(df, x="metric", y="value", text="value", color="metric")
    fig.update_layout(showlegend=False, yaxis_range=[0, 1], xaxis_title="", yaxis_title="Score")
    _apply_theme_layout(fig)
    st.plotly_chart(fig, use_container_width=True)
