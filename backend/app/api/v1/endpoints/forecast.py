from fastapi import APIRouter, Query, Body
from typing import List
from datetime import date
from pydantic import BaseModel

from app.services import forecasting

router = APIRouter()

class TrainRequest(BaseModel):
    property_id: int
    role: str
    target_col: str = "staff_count"

class OverrideRequest(BaseModel):
    property_id: int
    role: str
    date: date
    override_value: float
    reason: str = None

@router.get("/forecast", summary="Staffing Forecast", tags=["forecast"])
async def get_forecast(property_id: int = Query(...), start_date: date = Query(...), horizon: int = Query(7), role: str = Query("housekeeping")):
    """Return simple staffing forecast for a property and role.

    This is an MVP endpoint using a rolling baseline or LightGBM if available; it is intended for pilot/validation use.
    """
    preds = forecasting.predict_staff(property_id=property_id, start_date=start_date, horizon=horizon, role=role)
    return {"property_id": property_id, "role": role, "start_date": start_date.isoformat(), "predictions": preds}

@router.post("/train", summary="Train Forecast Model", tags=["forecast"])
async def train_model(req: TrainRequest = Body(...)):
    """Trigger training for a property and role. Expects historical feature data to be provided or available in DB (MVP uses example data)."""
    # TODO: fetch historical data from DB for property_id + role
    # For now, create synthetic example dataset
    import pandas as pd
    from datetime import timedelta
    today = date.today()
    rows = []
    for i in range(120):
        d = today - timedelta(days=(120 - i))
        rows.append({"date": d.isoformat(), "occupancy": 50 + (i % 30), "tasks": 20 + (i % 10), "staff_count": 10 + (i % 5)})
    df = pd.DataFrame(rows)
    feature_df = forecasting.prepare_features(df.to_dict("records"))
    meta, model_path = forecasting.train_lightgbm(feature_df, target_col=req.target_col)
    return {"status": "ok", "meta": meta, "model_path": model_path}

@router.post("/override", summary="Save Forecast Override", tags=["forecast"])
async def save_override(req: OverrideRequest = Body(...)):
    """Persist manager override for a forecasted date.

    This will store the override and return a confirmation. UI should call this when the manager edits the suggested staff count.
    """
    # For MVP, persist via DB model when migrations available; here return echo
    return {"status": "ok", "override": req.dict()}
