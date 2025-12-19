from fastapi import APIRouter, Query
from typing import List
from datetime import date

from app.services import forecasting

router = APIRouter()

@router.get("/forecast", summary="Staffing Forecast", tags=["forecast"])
async def get_forecast(property_id: int = Query(...), start_date: date = Query(...), horizon: int = Query(7), role: str = Query("housekeeping")):
    """Return simple staffing forecast for a property and role.

    This is an MVP endpoint using a rolling baseline; it is intended for pilot/validation use.
    """
    preds = forecasting.predict_staff(property_id=property_id, start_date=start_date, horizon=horizon, role=role)
    return {"property_id": property_id, "role": role, "start_date": start_date.isoformat(), "predictions": preds}
