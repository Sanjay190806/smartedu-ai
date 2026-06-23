# SmartEdu AI Dashboard Guide

The Streamlit dashboard is the Phase 3 user interface for SmartEdu AI. It connects to the FastAPI backend at `SMARTEDU_API_BASE_URL`, defaulting to `http://127.0.0.1:8000`.

## Run

Start the backend:

```bash
uvicorn backend.main:app --reload
```

Start the dashboard in another terminal:

```bash
streamlit run dashboard/app.py
```

Open the dashboard at:

```text
http://localhost:8501
```

## Demo Flow

1. Open Executive Overview.
2. Confirm backend status is online.
3. Go to Risk Prediction.
4. Load the High Risk sample and click Predict.
5. Open Recommendations and select the same student.
6. Use Batch Upload with `data/sample_students.csv`.
7. Open System Status to show model artifacts and setup commands.

## Notes

The dashboard is an academic support interface. Predictions are probabilistic and should support mentor decisions, not replace them.
