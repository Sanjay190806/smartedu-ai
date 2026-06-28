from __future__ import annotations

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pandas as pd
import streamlit as st

from dashboard import api_client
from dashboard.components.cards import render_empty_state, render_info_card, render_metric_card
from dashboard.components.charts import risk_distribution_chart
from dashboard.components.layout import render_page_header, render_sidebar
from dashboard.components.tables import high_risk_table, predictions_table
from dashboard.config import REQUIRED_STUDENT_COLUMNS
from dashboard.utils.validators import validate_csv_columns


st.set_page_config(page_title="Batch Upload", layout="wide")
render_sidebar()
render_page_header("Batch Upload", "Upload CSV student data and run batch academic risk prediction.")

render_info_card(
    "Upload Instructions",
    "Upload a CSV with the Phase 1 student schema. If risk_label is present, the backend ignores it for prediction.",
    icon="CSV",
)
with st.expander("Required columns"):
    st.write(", ".join(REQUIRED_STUDENT_COLUMNS))

upload_col, sample_col = st.columns(2)
with upload_col:
    st.markdown("<div class='smart-card'><div class='section-title' style='margin-top:0'>Upload Your CSV</div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Choose CSV", type=["csv"])
    st.markdown("</div>", unsafe_allow_html=True)
with sample_col:
    st.markdown("<div class='smart-card'><div class='section-title' style='margin-top:0'>Use Demo Dataset</div>", unsafe_allow_html=True)
    use_sample = st.button("Use sample_students.csv", use_container_width=True)
    st.caption("Loads the local synthetic dataset for a fast demo.")
    st.markdown("</div>", unsafe_allow_html=True)

df = None
file_name = None
if uploaded is not None:
    file_name = uploaded.name
    df = pd.read_csv(uploaded)
elif use_sample:
    sample_path = ROOT / "data" / "sample_students.csv"
    if sample_path.exists():
        file_name = "sample_students.csv"
        df = pd.read_csv(sample_path)
    else:
        st.warning("data/sample_students.csv was not found.")

if df is None:
    render_empty_state("No dataset loaded", "Upload a CSV or use the demo dataset to begin batch prediction.")
else:
    ok, missing = validate_csv_columns(df)
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        render_metric_card("Rows", len(df), "Student records")
    with p2:
        render_metric_card("Columns", len(df.columns), "Dataset width")
    with p3:
        render_metric_card("Missing Required", len(missing), "Schema gaps", accent="#ef4444" if missing else "#22c55e")
    with p4:
        render_metric_card("Ready Status", "Ready" if ok else "Blocked", "Validation state", accent="#22c55e" if ok else "#ef4444")

    st.markdown("<div class='smart-card'><div class='section-title' style='margin-top:0'>CSV Preview</div>", unsafe_allow_html=True)
    st.dataframe(df.head(10), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if not ok:
        st.warning(f"Missing required columns: {', '.join(missing)}")
        st.stop()

    if st.button("Run Batch Prediction", type="primary", use_container_width=True):
        result = api_client.batch_predict(file_name or "upload.csv", df.to_csv(index=False).encode("utf-8"))
        if not result.get("ok"):
            st.warning(result.get("error"))
            st.stop()
        st.session_state.uploaded_batch_result = result["data"]
        st.success(f"Predicted {result['data']['total_records']} records.")

result = st.session_state.get("uploaded_batch_result")
if result:
    st.markdown("<div class='section-title'>Batch Results Dashboard</div>", unsafe_allow_html=True)
    dist = result.get("risk_distribution", {})
    b1, b2, b3, b4 = st.columns(4)
    with b1:
        render_metric_card("Total Records", result.get("total_records", 0), "Predicted rows")
    with b2:
        render_metric_card("High Risk", dist.get("High Risk", 0), "Priority students", accent="#ef4444")
    with b3:
        render_metric_card("Medium Risk", dist.get("Medium Risk", 0), "Monitor group", accent="#f59e0b")
    with b4:
        render_metric_card("Low Risk", dist.get("Low Risk", 0), "Stable group", accent="#22c55e")

    c1, c2 = st.columns(2)
    with c1:
        risk_distribution_chart(dist)
    with c2:
        risk_distribution_chart(dist, chart_type="pie")

    predictions = result.get("predictions", [])
    st.markdown("<div class='section-title'>High-Risk Student Spotlight</div>", unsafe_allow_html=True)
    high_risk_table(predictions)
    st.markdown("<div class='section-title'>Full Prediction Report</div>", unsafe_allow_html=True)
    prediction_df = predictions_table(predictions)
    d1, d2 = st.columns(2)
    d1.download_button("Download CSV Report", prediction_df.to_csv(index=False), "batch_predictions.csv", "text/csv", use_container_width=True)
    d2.download_button("Download JSON Report", json.dumps(result, indent=2), "batch_predictions.json", "application/json", use_container_width=True)
