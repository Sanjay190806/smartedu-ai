from __future__ import annotations

from pathlib import Path
import json
import sys

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_recall_fscore_support

from ml.preprocessing import (
    DEFAULT_DATA_PATH,
    RISK_LABELS,
    build_preprocessor,
    create_train_test_split,
    get_feature_names,
    load_dataset,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_REGISTRY = PROJECT_ROOT / "ml" / "model_registry"


def evaluate_candidate(name: str, model, x_test, y_test) -> dict:
    predictions = model.predict(x_test)
    precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
        y_test, predictions, average="macro", zero_division=0
    )
    report = classification_report(y_test, predictions, output_dict=True, zero_division=0)
    high_risk_recall = report.get("High Risk", {}).get("recall", 0.0)
    selection_score = (0.7 * f1_macro) + (0.3 * high_risk_recall)
    return {
        "model_name": name,
        "accuracy": accuracy_score(y_test, predictions),
        "precision_macro": precision_macro,
        "recall_macro": recall_macro,
        "f1_macro": f1_macro,
        "high_risk_recall": high_risk_recall,
        "selection_score": selection_score,
        "classification_report": report,
        "confusion_matrix": confusion_matrix(y_test, predictions, labels=RISK_LABELS).tolist(),
    }


def train(data_path: Path = DEFAULT_DATA_PATH) -> dict:
    df = load_dataset(data_path)
    x_train, x_test, y_train, y_test = create_train_test_split(df)

    preprocessor = build_preprocessor()
    x_train_processed = preprocessor.fit_transform(x_train)
    x_test_processed = preprocessor.transform(x_test)

    candidates = {
        "Logistic Regression": LogisticRegression(max_iter=1200, class_weight="balanced", random_state=42),
        "Random Forest": RandomForestClassifier(
            n_estimators=250,
            class_weight="balanced",
            random_state=42,
            min_samples_leaf=2,
        ),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42),
    }

    trained_models = {}
    metrics_by_model = {}
    for name, model in candidates.items():
        model.fit(x_train_processed, y_train)
        trained_models[name] = model
        metrics_by_model[name] = evaluate_candidate(name, model, x_test_processed, y_test)

    best_name = max(metrics_by_model, key=lambda name: metrics_by_model[name]["selection_score"])
    best_model = trained_models[best_name]
    feature_names = get_feature_names(preprocessor)

    MODEL_REGISTRY.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_model, MODEL_REGISTRY / "model.joblib")
    joblib.dump(preprocessor, MODEL_REGISTRY / "preprocessor.joblib")
    (MODEL_REGISTRY / "feature_names.json").write_text(
        json.dumps(feature_names, indent=2),
        encoding="utf-8",
    )

    metrics = {
        "best_model": best_name,
        "selection_policy": "0.7 * macro F1 + 0.3 * High Risk recall",
        "label_order": RISK_LABELS,
        "records": int(len(df)),
        "train_records": int(len(y_train)),
        "test_records": int(len(y_test)),
        "models": metrics_by_model,
    }
    (MODEL_REGISTRY / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def main() -> None:
    metrics = train()
    best = metrics["best_model"]
    best_metrics = metrics["models"][best]
    print(f"Best model: {best}")
    print(f"Macro F1: {best_metrics['f1_macro']:.3f}")
    print(f"High Risk recall: {best_metrics['high_risk_recall']:.3f}")
    print(f"Artifacts saved to {MODEL_REGISTRY}")


if __name__ == "__main__":
    main()
