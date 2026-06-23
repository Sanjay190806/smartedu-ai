from __future__ import annotations

from io import BytesIO

import pandas as pd

from ml.preprocessing import FEATURE_COLUMNS


CSV_REQUIRED_COLUMNS = ["student_id", "name"] + FEATURE_COLUMNS


def validate_csv_columns(df: pd.DataFrame) -> None:
    missing = sorted(set(CSV_REQUIRED_COLUMNS) - set(df.columns))
    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")


def dataframe_from_upload(file_bytes: bytes) -> pd.DataFrame:
    try:
        df = pd.read_csv(BytesIO(file_bytes))
    except Exception as exc:
        raise ValueError("Uploaded file must be a valid CSV.") from exc
    validate_csv_columns(df)
    return df


def ensure_unique_student_ids(df: pd.DataFrame) -> None:
    if df["student_id"].duplicated().any():
        duplicates = df.loc[df["student_id"].duplicated(), "student_id"].unique().tolist()
        raise ValueError(f"CSV contains duplicate student_id values: {duplicates[:5]}")
