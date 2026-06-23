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
from dashboard.components.layout import render_page_header, render_sidebar


st.set_page_config(page_title="Recommendations", layout="wide")
render_sidebar()
render_page_header("Recommendations", "Personalized academic guidance for mentors and students.")

students = api_client.get_students()
if not students.get("ok"):
    st.warning(students.get("error"))
    st.stop()
if not students.get("data"):
    st.info("No students found yet. Run a prediction first.")
    st.stop()

student_options = {f"{s['student_id']} - {s['name']}": s for s in students["data"]}
selected = st.selectbox("Select student", list(student_options.keys()))
student = student_options[selected]
student_id = student["student_id"]

recommendation = api_client.get_recommendation(student_id)
if not recommendation.get("ok"):
    st.info("No recommendation found yet. Run a prediction first.")
    if st.button("Generate recommendation from latest academic record"):
        record = student.get("latest_academic_record") or {}
        payload = {**{k: student[k] for k in ["student_id", "name", "department", "year", "semester", "gender"]}, **record}
        payload.pop("id", None)
        payload.pop("created_at", None)
        result = api_client.predict_student(payload)
        if result.get("ok"):
            recommendation = {"ok": True, "data": result["data"]["recommendations"]}
        else:
            st.warning(result.get("error"))
            st.stop()

if recommendation.get("ok"):
    rec = recommendation["data"]
    risk_badge(rec.get("risk_category", "Medium Risk"))
    st.write(rec.get("summary"))
    tab1, tab2, tab3 = st.tabs(["Priorities", "Plans", "Mentor Copy"])
    with tab1:
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
        st.markdown("**Resources**")
        for item in rec.get("resources", []):
            st.write(f"- {item}")
        st.info(rec.get("mentor_note", ""))
    with tab3:
        mentor_text = (
            f"Student: {student.get('name')} ({student_id})\n"
            f"Risk: {rec.get('risk_category')}\n\n"
            f"Main issues:\n" + "\n".join(f"- {item}" for item in rec.get("top_problems", [])) + "\n\n"
            f"Next 7 days:\n" + "\n".join(f"- {item}" for item in rec.get("seven_day_plan", [])) + "\n\n"
            f"Mentor note:\n{rec.get('mentor_note', '')}"
        )
        st.text_area("Mentor note draft", mentor_text, height=260)
        st.download_button("Download recommendation text", mentor_text, f"{student_id}_recommendation.txt", "text/plain")
        st.download_button("Download recommendation JSON", json.dumps(rec, indent=2), f"{student_id}_recommendation.json", "application/json")
