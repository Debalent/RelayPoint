from fastapi import APIRouter, Query, Body
from typing import List
from datetime import date
from pydantic import BaseModel
from sqlalchemy.orm import Session

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

from app.db import get_db
from fastapi import Depends

@router.post("/train", summary="Train Forecast Model", tags=["forecast"])
async def train_model(req: TrainRequest = Body(...), db: Session = Depends(get_db)):
    """Trigger training for a property and role. Uses available historical data in the DB."""
    # Attempt to fetch historical rows from DB
    rows = forecasting.fetch_historical_dataset(db, property_id=req.property_id, role=req.role)
    if not rows:
        # Fallback to synthetic short dataset but notify client
        from datetime import timedelta
        today = date.today()
        rows = []
        for i in range(120):
            d = today - timedelta(days=(120 - i))
            rows.append({"date": d.isoformat(), "occupancy": 50 + (i % 30), "tasks": 20 + (i % 10), "staff_count": 10 + (i % 5)})

    feature_df = forecasting.prepare_features(rows)
    meta, model_path = forecasting.train_lightgbm(feature_df, target_col=req.target_col)

    # Optionally record metadata in DB
    try:
        crud_forecasting.create_model_record(db, property_id=req.property_id, role=req.role, model_type='lightgbm', path=model_path, metadata=meta)
    except Exception:
        # non-blocking if DB record fails
        pass

    return {"status": "ok", "meta": meta, "model_path": model_path}

from app.db import get_db
from fastapi import Depends, HTTPException
from app.schemas.forecasting import ForecastOverrideCreate, ForecastOverrideOut
from app.crud import forecasting as crud_forecasting


@router.post("/override", response_model=ForecastOverrideOut, summary="Save Forecast Override", tags=["forecast"])
async def save_override(req: ForecastOverrideCreate = Body(...), db: Session = Depends(get_db)):
    """Persist manager override for a forecasted date.

    Stores the override in the database and returns the saved record.
    """
    try:
        ov = crud_forecasting.create_override(db, property_id=req.property_id, role=req.role, date=req.date.isoformat(), override_value=req.override_value, reason=req.reason)
        return ov
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
