from __future__ import annotations

import streamlit as st

from dashboard.api_client import BACKEND_OFFLINE_ERROR


def backend_offline_message() -> None:
    st.warning(BACKEND_OFFLINE_ERROR)


def empty_state(message: str) -> None:
    st.info(message)


def success_message(message: str) -> None:
    st.success(message)


def warning_message(message: str) -> None:
    st.warning(message)


def error_message(message: str) -> None:
    st.error(message)
