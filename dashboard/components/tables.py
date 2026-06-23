from __future__ import annotations

import pandas as pd
import streamlit as st


def students_table(students: list[dict]) -> pd.DataFrame:
    rows = []
    for student in students:
        record = student.get("latest_academic_record") or {}
        rows.append(
            {
                "student_id": student.get("student_id"),
                "name": student.get("name"),
                "department": student.get("department"),
                "year": student.get("year"),
                "semester": student.get("semester"),
                "gender": student.get("gender"),
                "current_gpa": record.get("current_gpa"),
                "attendance_percentage": record.get("attendance_percentage"),
            }
        )
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
    return df


def predictions_table(predictions: list[dict]) -> pd.DataFrame:
    rows = [
        {
            "student_id": item.get("student_id"),
            "risk_category": item.get("risk_category"),
            "probability": item.get("probability"),
            "confidence": item.get("confidence"),
            "top_factors": "; ".join(item.get("top_factors", [])[:3]),
        }
        for item in predictions
    ]
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
    return df


def high_risk_table(predictions: list[dict]) -> pd.DataFrame:
    high_risk = [item for item in predictions if item.get("risk_category") == "High Risk"]
    return predictions_table(high_risk)
