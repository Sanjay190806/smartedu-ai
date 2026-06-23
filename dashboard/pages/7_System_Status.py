from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from dashboard import api_client
from dashboard.components.cards import status_badge
from dashboard.components.layout import render_page_header, render_sidebar


st.set_page_config(page_title="System Status", layout="wide")
render_sidebar()
render_page_header("System Status", "Technical health, API routes, and model artifact readiness.")

health = api_client.check_backend_health()
status_badge("Backend", bool(health.get("ok")))
if health.get("ok"):
    st.json(health["data"], expanded=False)
else:
    st.warning(health.get("error"))

st.subheader("API Route Checklist")
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
for route in routes:
    st.write(f"- {route}")

st.subheader("Model Metrics")
metrics_path = ROOT / "ml" / "model_registry" / "metrics.json"
if metrics_path.exists():
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    best = metrics.get("best_model")
    best_metrics = metrics.get("models", {}).get(best, {})
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Selected model", best or "-")
    c2.metric("Macro F1", f"{best_metrics.get('f1_macro', 0):.3f}")
    c3.metric("High-risk recall", f"{best_metrics.get('high_risk_recall', 0):.3f}")
    c4.metric("Accuracy", f"{best_metrics.get('accuracy', 0):.3f}")
else:
    st.warning("ml/model_registry/metrics.json was not found.")

st.subheader("Artifact Status")
artifacts = [
    "ml/model_registry/model.joblib",
    "ml/model_registry/preprocessor.joblib",
    "ml/model_registry/metrics.json",
    "ml/model_registry/feature_names.json",
    "data/sample_students.csv",
]
for artifact in artifacts:
    st.write(f"- {artifact}: {'Found' if (ROOT / artifact).exists() else 'Missing'}")

st.subheader("Setup Commands")
st.code("uvicorn backend.main:app --reload", language="bash")
st.code("streamlit run dashboard/app.py", language="bash")
st.code("python -m pytest", language="bash")
