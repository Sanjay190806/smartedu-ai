from __future__ import annotations

from pathlib import Path
import json
import sys

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

import joblib
from sklearn.metrics import classification_report, confusion_matrix

from ml.explainability import get_feature_importance
from ml.preprocessing import DEFAULT_DATA_PATH, RISK_LABELS, create_train_test_split, load_dataset


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_REGISTRY = PROJECT_ROOT / "ml" / "model_registry"


def evaluate(data_path: Path = DEFAULT_DATA_PATH) -> dict:
    model_path = MODEL_REGISTRY / "model.joblib"
    preprocessor_path = MODEL_REGISTRY / "preprocessor.joblib"
    if not model_path.exists() or not preprocessor_path.exists():
        raise FileNotFoundError("Model artifacts are missing. Run: python ml/train_model.py")

    model = joblib.load(model_path)
    preprocessor = joblib.load(preprocessor_path)
    df = load_dataset(data_path)
    _, x_test, _, y_test = create_train_test_split(df)
    x_test_processed = preprocessor.transform(x_test)
    predictions = model.predict(x_test_processed)

    report = classification_report(y_test, predictions, output_dict=True, zero_division=0)
    matrix = confusion_matrix(y_test, predictions, labels=RISK_LABELS).tolist()
    results = {
        "classification_report": report,
        "confusion_matrix": matrix,
        "label_order": RISK_LABELS,
        "feature_importance_top_15": get_feature_importance(),
    }
    (MODEL_REGISTRY / "evaluation_report.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    return results


def main() -> None:
    results = evaluate()
    print("Classification report:")
    print(json.dumps(results["classification_report"], indent=2))
    print("Confusion matrix label order:", results["label_order"])
    print(results["confusion_matrix"])


if __name__ == "__main__":
    main()
