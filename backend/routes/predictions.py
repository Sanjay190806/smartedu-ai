from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import ValidationError
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.prediction_schema import BatchPredictionResponse, PredictionRequest, PredictionResponse
from backend.schemas.student_schema import StudentAcademicPayload
from backend.services.prediction_service import ModelArtifactError, predict_and_persist
from backend.utils.validators import dataframe_from_upload, ensure_unique_student_ids


router = APIRouter(prefix="/predict", tags=["Predictions"])


@router.post("", response_model=PredictionResponse)
def predict_student(payload: PredictionRequest, db: Session = Depends(get_db)):
    try:
        return predict_and_persist(db, payload)
    except ModelArtifactError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/batch", response_model=BatchPredictionResponse)
async def batch_predict(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV uploads are supported.")
    try:
        df = dataframe_from_upload(await file.read())
        ensure_unique_student_ids(df)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    predictions = []
    risk_distribution = {"Low Risk": 0, "Medium Risk": 0, "High Risk": 0}
    for record in df.to_dict(orient="records"):
        record.pop("risk_label", None)
        try:
            payload = StudentAcademicPayload(**record)
            result = predict_and_persist(db, payload)
        except ValidationError as exc:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid row for student_id={record.get('student_id')}: {exc.errors()}",
            ) from exc
        except ModelArtifactError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        predictions.append(result)
        risk_distribution[result["risk_category"]] = risk_distribution.get(result["risk_category"], 0) + 1

    return {
        "total_records": len(predictions),
        "predictions": predictions,
        "risk_distribution": risk_distribution,
    }
