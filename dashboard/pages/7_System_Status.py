from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from dashboard import api_client
from dashboard.components.cards import render_command_card, render_metric_card, render_status_card
from dashboard.components.layout import render_page_header, render_sidebar


st.set_page_config(page_title="System Status", layout="wide")
render_sidebar()
render_page_header("System Status", "Technical health dashboard for backend, model artifacts, and runtime commands.")

health = api_client.check_backend_health()
data = health.get("data", {}) if health.get("ok") else {}
c1, c2, c3, c4 = st.columns(4)
with c1:
    render_status_card("Backend", bool(health.get("ok")), data.get("service", health.get("error", "")))
with c2:
    render_metric_card("Service", data.get("service", "Unavailable"), "FastAPI application")
with c3:
    render_metric_card("Phase", data.get("phase", "-"), "Backend phase")
with c4:
    render_status_card("Model Loaded", bool(data.get("model_loaded")), f"Loaded: {data.get('model_loaded', False)}")

st.markdown("<div class='section-title'>API Route Checklist</div>", unsafe_allow_html=True)
routes = [
    "/health",
    "/students",
    "/predict",
    "/predict/batch",
    "/recommendations/{student_id}",
    "/analytics/summary",
    "/analytics/risk-distribution",
    "/analytics/subject-performance",
]
cols = st.columns(4)
for index, route in enumerate(routes):
    with cols[index % 4]:
        st.markdown(f"<div class='smart-card'><span class='small-label'>Route</span><br><strong>{route}</strong></div>", unsafe_allow_html=True)

st.markdown("<div class='section-title'>Model Metrics</div>", unsafe_allow_html=True)
metrics_path = ROOT / "ml" / "model_registry" / "metrics.json"
if metrics_path.exists():
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    best = metrics.get("best_model")
    best_metrics = metrics.get("models", {}).get(best, {})
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_metric_card("Best Model", best or "-", "Selected by F1 + recall")
    with m2:
        render_metric_card("Macro F1", f"{best_metrics.get('f1_macro', 0):.3f}", "Balanced class quality")
    with m3:
        render_metric_card("High Risk Recall", f"{best_metrics.get('high_risk_recall', 0):.3f}", "Intervention sensitivity")
    with m4:
        render_metric_card("Accuracy", f"{best_metrics.get('accuracy', 0):.3f}", "Held-out test split")
else:
    st.warning("ml/model_registry/metrics.json was not found.")

st.markdown("<div class='section-title'>Artifact Status</div>", unsafe_allow_html=True)
artifacts = [
    "ml/model_registry/model.joblib",
    "ml/model_registry/preprocessor.joblib",
    "ml/model_registry/metrics.json",
    "ml/model_registry/feature_names.json",
    "ml/model_registry/evaluation_report.json",
    "data/sample_students.csv",
]
artifact_cols = st.columns(3)
for index, artifact in enumerate(artifacts):
    with artifact_cols[index % 3]:
        exists = (ROOT / artifact).exists()
        render_status_card(artifact, exists, "Found" if exists else "Missing")

st.markdown("<div class='section-title'>Setup Commands</div>", unsafe_allow_html=True)
cmd1, cmd2, cmd3 = st.columns(3)
with cmd1:
    render_command_card("Backend", "uvicorn backend.main:app --reload")
with cmd2:
    render_command_card("Dashboard", "streamlit run dashboard/app.py")
with cmd3:
    render_command_card("Tests", "python -m pytest")
