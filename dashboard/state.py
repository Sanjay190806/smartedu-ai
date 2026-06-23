from __future__ import annotations

import streamlit as st


DEFAULTS = {
    "latest_prediction": None,
    "selected_student_id": None,
    "uploaded_batch_result": None,
    "backend_status": None,
    "active_sample_payload": None,
}


def initialize_state() -> None:
    for key, value in DEFAULTS.items():
        st.session_state.setdefault(key, value)
