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
from dashboard.components.charts import risk_distribution_chart
from dashboard.components.layout import render_page_header, render_sidebar
from dashboard.components.tables import high_risk_table, predictions_table
from dashboard.config import REQUIRED_STUDENT_COLUMNS
from dashboard.utils.validators import validate_csv_columns


st.set_page_config(page_title="Batch Upload", layout="wide")
render_sidebar()
render_page_header("Batch Upload", "Upload a CSV file and run backend batch predictions.")

st.expander("Required columns").write(", ".join(REQUIRED_STUDENT_COLUMNS))
uploaded = st.file_uploader("Upload CSV", type=["csv"])
use_sample = st.button("Use sample_students.csv")

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

if df is not None:
    st.metric("Rows", len(df))
    st.metric("Columns", len(df.columns))
    st.dataframe(df.head(10), use_container_width=True, hide_index=True)
    ok, missing = validate_csv_columns(df)
    if not ok:
        st.error(f"Missing required columns: {', '.join(missing)}")
        st.stop()
    if st.button("Run Batch Prediction", type="primary"):
        result = api_client.batch_predict(file_name or "upload.csv", df.to_csv(index=False).encode("utf-8"))
        if not result.get("ok"):
            st.warning(result.get("error"))
            st.stop()
        data = result["data"]
        st.session_state.uploaded_batch_result = data
        st.success(f"Predicted {data['total_records']} records.")

result = st.session_state.get("uploaded_batch_result")
if result:
    st.subheader("Batch Results")
    c1, c2 = st.columns(2)
    with c1:
        risk_distribution_chart(result.get("risk_distribution", {}))
    with c2:
        risk_distribution_chart(result.get("risk_distribution", {}), chart_type="pie")
    predictions = result.get("predictions", [])
    prediction_df = predictions_table(predictions)
    st.subheader("High-Risk Students")
    high_risk_table(predictions)
    st.download_button("Download predictions CSV", prediction_df.to_csv(index=False), "batch_predictions.csv", "text/csv")
    st.download_button("Download predictions JSON", json.dumps(result, indent=2), "batch_predictions.json", "application/json")
