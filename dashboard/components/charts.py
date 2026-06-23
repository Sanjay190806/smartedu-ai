from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from dashboard.config import RISK_COLORS


def risk_distribution_chart(distribution: dict[str, int], chart_type: str = "bar") -> None:
    df = pd.DataFrame(
        [{"risk": risk, "count": int(count)} for risk, count in distribution.items()]
    )
    if df.empty or df["count"].sum() == 0:
        st.info("No prediction records found yet. Run a prediction or upload a batch CSV.")
        return
    if chart_type == "pie":
        fig = px.pie(df, values="count", names="risk", hole=0.45, color="risk", color_discrete_map=RISK_COLORS)
    else:
        fig = px.bar(df, x="risk", y="count", color="risk", color_discrete_map=RISK_COLORS, text="count")
        fig.update_layout(xaxis_title="", yaxis_title="Students")
    st.plotly_chart(fig, use_container_width=True)


def subject_performance_chart(subjects: dict[str, float]) -> None:
    df = pd.DataFrame([{"subject": key.title(), "score": value} for key, value in subjects.items()])
    fig = px.bar(df, x="subject", y="score", text="score", color="subject")
    fig.update_layout(showlegend=False, yaxis_range=[0, 100], xaxis_title="", yaxis_title="Average score")
    st.plotly_chart(fig, use_container_width=True)


def weak_subjects_chart(subjects: list[str]) -> None:
    if not subjects:
        st.info("Weak subject insight is not available yet.")
        return
    df = pd.DataFrame({"subject": [subject.title() for subject in subjects], "rank": list(range(1, len(subjects) + 1))})
    fig = px.bar(df, x="rank", y="subject", orientation="h", text="subject")
    fig.update_layout(showlegend=False, xaxis_title="Priority rank", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)


def attendance_gpa_scatter(df: pd.DataFrame) -> None:
    if df.empty or not {"attendance_percentage", "current_gpa"}.issubset(df.columns):
        st.info("Attendance vs GPA data is not available.")
        return
    fig = px.scatter(df, x="attendance_percentage", y="current_gpa", hover_data=["student_id", "name"])
    fig.update_layout(xaxis_title="Attendance %", yaxis_title="Current GPA")
    st.plotly_chart(fig, use_container_width=True)


def ranked_factors_chart(factors: list[str]) -> None:
    if not factors:
        st.info("No top factors returned for this prediction.")
        return
    fig = go.Figure(go.Bar(x=list(range(len(factors), 0, -1)), y=factors, orientation="h"))
    fig.update_layout(xaxis_title="Relative rank", yaxis_title="", height=max(260, 50 * len(factors)))
    st.plotly_chart(fig, use_container_width=True)
