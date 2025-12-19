"""
Minimal forecasting service scaffold for staffing forecasts.
This module provides small, testable functions to prepare data, train a baseline model,
and produce predictions. It is intentionally lightweight for the MVP.

Planned enhancements:
- Add training pipeline using LightGBM or XGBoost
- Persist models and version metadata
- Add evaluation metrics and logging (MAE, MAPE, RMSE)
- Add Explainability (SHAP) for feature contributions

Example usage:
    from app.services.forecasting import predict_staff
    preds = predict_staff(property_id, date, horizon=7, role='housekeeping')

"""
from typing import Dict, List, Any
from datetime import date, datetime


def prepare_features(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Normalize and create lag features from raw event rows.

    events: list of dicts with keys like 'timestamp', 'occupancy', 'tasks'
    returns: list of feature dicts ready for model ingestion
    """
    # TODO: implement actual transformation
    features = []
    for ev in events:
        features.append({
            "date": ev.get("date"),
            "occupancy": ev.get("occupancy", 0),
            "tasks": ev.get("tasks", 0),
        })
    return features


def train_baseline(feature_rows: List[Dict[str, Any]], target: str = "staff_count") -> Dict[str, Any]:
    """Train a simple baseline model (rolling mean) and return model metadata.

    This is a placeholder for the MVP; replace with LightGBM or similar later.
    """
    # naive baseline: average of last N values
    values = [r.get(target, 0) for r in feature_rows if target in r]
    avg = sum(values) / len(values) if values else 0
    model = {"type": "rolling_mean", "value": avg}
    return model


def predict(model: Dict[str, Any], features: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Produce predictions for each feature row with a confidence estimate.

    Returns list of dicts: {date, predicted, lower, upper}
    """
    preds = []
    base = model.get("value", 0)
    for f in features:
        preds.append({
            "date": f.get("date"),
            "predicted": base,
            "lower": max(0, base * 0.8),
            "upper": base * 1.2,
            "model": model.get("type"),
        })
    return preds


def predict_staff(property_id: int, start_date: date, horizon: int = 7, role: str = "housekeeping") -> List[Dict[str, Any]]:
    """High-level helper to fetch data, prepare features, and return predictions.

    For the MVP, this uses a trivial baseline model and returns a prediction for each day in the horizon.
    """
    # TODO: fetch events from DB (occupancy, tasks, staff logs) for property_id
    # For now, create dummy daily rows
    days = []
    for i in range(horizon):
        d = start_date
        days.append({"date": d.isoformat(), "occupancy": 50 + i, "tasks": 20 + i})
    features = prepare_features(days)
    model = train_baseline([])
    preds = predict(model, features)
    return preds
