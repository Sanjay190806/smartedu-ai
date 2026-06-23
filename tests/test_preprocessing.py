import pandas as pd

from ml.preprocessing import FEATURE_COLUMNS, build_preprocessor, split_features_target, validate_dataset


def test_preprocessor_transforms_sample_frame():
    df = pd.read_csv("data/sample_students.csv").head(20)
    validate_dataset(df)
    x, y = split_features_target(df)
    preprocessor = build_preprocessor()
    transformed = preprocessor.fit_transform(x)

    assert len(y) == 20
    assert transformed.shape[0] == 20
    assert set(FEATURE_COLUMNS).issubset(set(x.columns))


def test_validation_rejects_missing_required_column():
    df = pd.read_csv("data/sample_students.csv").drop(columns=["risk_label"])
    try:
        validate_dataset(df)
    except ValueError as exc:
        assert "risk_label" in str(exc)
    else:
        raise AssertionError("validate_dataset should reject missing target column")
