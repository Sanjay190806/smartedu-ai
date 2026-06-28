from __future__ import annotations

from typing import Any

import requests

from dashboard.config import API_BASE_URL, REQUEST_TIMEOUT


BACKEND_OFFLINE_ERROR = "Backend is not running. Start it with: uvicorn backend.main:app --reload"


def _result(ok: bool, data: Any = None, error: str | None = None, status_code: int | None = None) -> dict[str, Any]:
    return {"ok": ok, "data": data, "error": error, "status_code": status_code}


def _extract_error(response: requests.Response) -> str:
    try:
        body = response.json()
    except ValueError:
        return response.text or f"HTTP {response.status_code}"
    detail = body.get("detail", body)
    if isinstance(detail, list):
        return "; ".join(str(item.get("msg", item)) for item in detail)
    return str(detail)


def _request(method: str, path: str, **kwargs) -> dict[str, Any]:
    try:
        response = requests.request(
            method,
            f"{API_BASE_URL}{path}",
            timeout=REQUEST_TIMEOUT,
            **kwargs,
        )
    except requests.RequestException:
        return _result(False, error=BACKEND_OFFLINE_ERROR)

    if response.status_code >= 400:
        return _result(False, error=_extract_error(response), status_code=response.status_code)
    try:
        return _result(True, data=response.json(), status_code=response.status_code)
    except ValueError:
        return _result(True, data=response.text, status_code=response.status_code)


def check_backend_health() -> dict[str, Any]:
    return _request("GET", "/health")


def get_root() -> dict[str, Any]:
    return _request("GET", "/")


def get_students() -> dict[str, Any]:
    return _request("GET", "/students")


def get_student(student_id: str) -> dict[str, Any]:
    return _request("GET", f"/students/{student_id}")


def create_student(payload: dict[str, Any]) -> dict[str, Any]:
    return _request("POST", "/students", json=payload)


def update_student(student_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return _request("PUT", f"/students/{student_id}", json=payload)


def delete_student(student_id: str) -> dict[str, Any]:
    return _request("DELETE", f"/students/{student_id}")


def predict_student(payload: dict[str, Any]) -> dict[str, Any]:
    return _request("POST", "/predict", json=payload)


def batch_predict(file_name: str, file_bytes: bytes) -> dict[str, Any]:
    files = {"file": (file_name, file_bytes, "text/csv")}
    return _request("POST", "/predict/batch", files=files)


def get_recommendation(student_id: str) -> dict[str, Any]:
    return _request("GET", f"/recommendations/{student_id}")


def generate_recommendation(payload: dict[str, Any]) -> dict[str, Any]:
    return _request("POST", "/recommendations/generate", json=payload)


def get_analytics_summary() -> dict[str, Any]:
    return _request("GET", "/analytics/summary")


def get_risk_distribution() -> dict[str, Any]:
    return _request("GET", "/analytics/risk-distribution")


def get_department_analytics(department: str) -> dict[str, Any]:
    return _request("GET", f"/analytics/department/{department}")


def get_subject_performance() -> dict[str, Any]:
    return _request("GET", "/analytics/subject-performance")


def get_mentor_provider_status() -> dict[str, Any]:
    return _request("GET", "/mentor/provider-status")


def list_mentor_sessions() -> dict[str, Any]:
    return _request("GET", "/mentor/sessions")


def start_mentor_session(payload: dict[str, Any]) -> dict[str, Any]:
    return _request("POST", "/mentor/start", json=payload)


def submit_mentor_answer(session_id: str, answer: str) -> dict[str, Any]:
    return _request("POST", f"/mentor/{session_id}/answer", json={"answer": answer})


def get_mentor_session(session_id: str) -> dict[str, Any]:
    return _request("GET", f"/mentor/{session_id}")


def generate_mentor_report(session_id: str) -> dict[str, Any]:
    return _request("POST", f"/mentor/{session_id}/report")


def get_mentor_report(session_id: str) -> dict[str, Any]:
    return _request("GET", f"/mentor/{session_id}/report")


def delete_mentor_session(session_id: str) -> dict[str, Any]:
    return _request("DELETE", f"/mentor/{session_id}")
