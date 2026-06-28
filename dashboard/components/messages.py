from __future__ import annotations

import streamlit as st

from dashboard.api_client import BACKEND_OFFLINE_ERROR
from dashboard.components.cards import render_empty_state


def backend_offline_message() -> None:
    backend_offline_panel()


def empty_state(message: str) -> None:
    render_empty_state("Nothing to show yet", message)


def success_message(message: str) -> None:
    success_banner(message)


def warning_message(message: str) -> None:
    warning_banner(message)


def error_message(message: str) -> None:
    error_banner(message)


def success_banner(message: str) -> None:
    st.success(message)


def warning_banner(message: str) -> None:
    st.warning(message)


def error_banner(message: str) -> None:
    st.error(message)


def info_banner(message: str) -> None:
    st.info(message)


def backend_offline_panel() -> None:
    render_empty_state(
        "Backend is offline",
        BACKEND_OFFLINE_ERROR,
        "Start the API, then refresh this dashboard.",
    )
