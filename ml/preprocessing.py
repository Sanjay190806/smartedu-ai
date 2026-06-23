from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_PATH = PROJECT_ROOT / "data" / "sample_students.csv"
TARGET_COLUMN = "risk_label"
IDENTIFIER_COLUMNS = ["student_id", "name"]

REQUIRED_COLUMNS = [
    "student_id", "name", "department", "year", "semester", "gender",
    "attendance_percentage", "internal_marks_average", "assignment_completion_rate",
    "quiz_average", "previous_semester_gpa", "current_gpa", "study_hours_per_week",
    "backlogs", "late_submissions", "participation_score", "subject_math_score",
    "subject_programming_score", "subject_electronics_score", "subject_communication_score",
    "subject_lab_score", "library_usage_hours", "lms_login_frequency",
    "parent_meeting_count", "mentor_meeting_count", "extracurricular_hours",
    "stress_level", "sleep_hours", "internet_access", "risk_label",
]

NUMERIC_FEATURES = [
    "year", "semester", "attendance_percentage", "internal_marks_average",
    "assignment_completion_rate", "quiz_average", "previous_semester_gpa",
    "current_gpa", "study_hours_per_week", "backlogs", "late_submissions",
    "participation_score", "subject_math_score", "subject_programming_score",
    "subject_electronics_score", "subject_communication_score", "subject_lab_score",
    "library_usage_hours", "lms_login_frequency", "parent_meeting_count",
    "mentor_meeting_count", "extracurricular_hours", "stress_level", "sleep_hours",
]
CATEGORICAL_FEATURES = ["department", "gender", "internet_access"]
FEATURE_COLUMNS = NUMERIC_FEATURES + CATEGORICAL_FEATURES
RISK_LABELS = ["Low Risk", "Medium Risk", "High Risk"]


def load_dataset(path: str | Path = DEFAULT_DATA_PATH) -> pd.DataFrame:
    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {dataset_path}. Run: python data/generate_sample_data.py"
        )
    df = pd.read_csv(dataset_path)
    validate_dataset(df)
    return df


def validate_dataset(df: pd.DataFrame) -> None:
    missing = sorted(set(REQUIRED_COLUMNS) - set(df.columns))
    if missing:
        raise ValueError(f"Dataset is missing required columns: {missing}")

    invalid_labels = sorted(set(df[TARGET_COLUMN].dropna()) - set(RISK_LABELS))
    if invalid_labels:
        raise ValueError(f"Invalid risk labels found: {invalid_labels}")


def split_features_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    validate_dataset(df)
    return df[FEATURE_COLUMNS].copy(), df[TARGET_COLUMN].copy()


def build_preprocessor() -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, NUMERIC_FEATURES),
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
        ]
    )


def create_train_test_split(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    x, y = split_features_target(df)
    return train_test_split(
        x,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )


def get_feature_names(preprocessor: ColumnTransformer) -> list[str]:
    try:
        return list(preprocessor.get_feature_names_out())
    except Exception:
        names: list[str] = list(NUMERIC_FEATURES)
        encoder = preprocessor.named_transformers_["categorical"].named_steps["encoder"]
        names.extend(encoder.get_feature_names_out(CATEGORICAL_FEATURES).tolist())
        return names


def coerce_student_record(student_data: dict) -> pd.DataFrame:
    missing = sorted(set(FEATURE_COLUMNS) - set(student_data))
    if missing:
        raise ValueError(f"Student record is missing required feature fields: {missing}")
    return pd.DataFrame([{column: student_data[column] for column in FEATURE_COLUMNS}])


def validate_feature_columns(columns: Iterable[str]) -> None:
    missing = sorted(set(FEATURE_COLUMNS) - set(columns))
    if missing:
        raise ValueError(f"Missing model feature columns: {missing}")
