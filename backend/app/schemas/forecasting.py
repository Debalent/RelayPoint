from pydantic import BaseModel
from typing import Optional
from datetime import date


class ForecastOverrideCreate(BaseModel):
    property_id: int
    role: str
    date: date
    override_value: float
    reason: Optional[str] = None


class ForecastOverrideOut(ForecastOverrideCreate):
    id: int
    created_at: Optional[str] = None

    class Config:
        orm_mode = True
