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
from typing import Dict, List, Any, Optional, Tuple
from datetime import date, datetime
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import lightgbm as lgb
import joblib
import os
from app.core.config import settings

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models", "forecasting")
os.makedirs(MODEL_DIR, exist_ok=True)


def prepare_features(events: List[Dict[str, Any]]) -> pd.DataFrame:
    """Normalize and create lag features from raw event rows.

    events: list of dicts with keys like 'date', 'occupancy', 'tasks', 'staff_count'
    returns: pandas DataFrame
    """
    df = pd.DataFrame(events)
    if df.empty:
        return df
    # Ensure date column
    df["date"] = pd.to_datetime(df["date"]).dt.date
    # Example lag features
    df = df.sort_values("date")
    df["occupancy_lag1"] = df["occupancy"].shift(1).fillna(0)
    df["tasks_lag1"] = df["tasks"].shift(1).fillna(0)
    df["dow"] = pd.to_datetime(df["date"]).dt.dayofweek
    return df.fillna(0)


def train_lightgbm(feature_df: pd.DataFrame, target_col: str = "staff_count") -> Tuple[dict, str]:
    """Train a LightGBM regressor on provided features and return metadata and path.

    Returns (metrics, model_path)
    """
    if feature_df.empty or target_col not in feature_df.columns:
        raise ValueError("Feature DataFrame must contain target column")

    X = feature_df.drop(columns=["date", target_col])
    y = feature_df[target_col]

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    train_data = lgb.Dataset(X_train, label=y_train)
    val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)

    params = {
        "objective": "regression",
        "metric": "l2",
        "verbosity": -1,
    }

    model = lgb.train(params, train_data, valid_sets=[train_data, val_data], early_stopping_rounds=20, num_boost_round=100)

    preds = model.predict(X_val)
    mae = mean_absolute_error(y_val, preds)
    rmse = mean_squared_error(y_val, preds, squared=False)

    # Save model
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    model_filename = f"forecast_model_{ts}.pkl"
    model_path = os.path.join(MODEL_DIR, model_filename)
    joblib.dump(model, model_path)

    meta = {"model_filename": model_filename, "mae": float(mae), "rmse": float(rmse), "trained_at": ts}
    return meta, model_path


def load_latest_model() -> Optional[Tuple[Any, str]]:
    """Load the latest model (by filename sort) if available"""
    files = [f for f in os.listdir(MODEL_DIR) if f.endswith('.pkl')]
    if not files:
        return None
    files.sort()
    latest = files[-1]
    path = os.path.join(MODEL_DIR, latest)
    model = joblib.load(path)
    return model, path


def predict(model: Dict[str, Any], features: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Produce predictions for each feature row with a confidence estimate.

    If a LightGBM model object is passed in, use it; otherwise fallback to rolling baseline.
    Returns list of dicts: {date, predicted, lower, upper}
    """
    preds = []
    # If model is a LightGBM Booster
    if hasattr(model, "predict"):
        df = pd.DataFrame(features)
        if "date" in df.columns:
            dates = df["date"].tolist()
            X = df.drop(columns=["date"]) if "date" in df.columns else df
        else:
            dates = [f.get("date") for f in features]
            X = df
        values = model.predict(X)
        for d, v in zip(dates, values):
            preds.append({"date": d, "predicted": float(v), "lower": max(0, float(v) * 0.9), "upper": float(v) * 1.1, "model": "lightgbm"})
        return preds

    # Fallback to baseline
    base = model.get("value", 0) if isinstance(model, dict) else 0
    for f in features:
        preds.append({
            "date": f.get("date"),
            "predicted": base,
            "lower": max(0, base * 0.8),
            "upper": base * 1.2,
            "model": model.get("type") if isinstance(model, dict) else "baseline",
        })
    return preds


def predict_staff(property_id: int, start_date: date, horizon: int = 7, role: str = "housekeeping") -> List[Dict[str, Any]]:
    """High-level helper to fetch data, prepare features, and return predictions.

    This will attempt to load the latest model; if none exists, fallback to rolling baseline.
    """
    # TODO: fetch events from DB (occupancy, tasks, staff logs) for property_id
    # For now, create dummy daily rows
    days = []
    for i in range(horizon):
        d = start_date
        days.append({"date": d.isoformat(), "occupancy": 50 + i, "tasks": 20 + i})
    features = prepare_features(days)

    model_loaded = load_latest_model()
    if model_loaded:
        model, path = model_loaded
        preds = predict(model, features)
    else:
        baseline = {"type": "rolling_mean", "value": features["occupancy"].mean() if not features.empty else 10}
        preds = predict(baseline, features.to_dict("records") if not features.empty else days)
    return preds
