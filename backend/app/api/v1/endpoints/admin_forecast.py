from fastapi import APIRouter, Depends, Query
from typing import List
from sqlalchemy.orm import Session
from app.db import get_db
from app.crud import forecasting as crud

router = APIRouter()

@router.get('/models', summary='List forecast models')
async def list_models(property_id: int = Query(None), db: Session = Depends(get_db)):
    # Very small helper to list models; using raw SQL for simplicity
    q = "SELECT id, property_id, role, model_type, version, metadata, path, created_at FROM forecast_models"
    if property_id:
        q += " WHERE property_id = :pid"
        res = db.execute(q, {"pid": property_id})
    else:
        res = db.execute(q)
    models = [dict(r) for r in res]
    return {"models": models}

@router.get('/predictions', summary='Recent forecast predictions')
async def list_predictions(property_id: int = Query(None), db: Session = Depends(get_db)):
    q = "SELECT id, property_id, role, date, predicted, lower, upper, model_id, created_at FROM forecast_predictions ORDER BY date DESC LIMIT 200"
    if property_id:
        q = q.replace('LIMIT 200', 'WHERE property_id = :pid ORDER BY date DESC LIMIT 200')
        res = db.execute(q, {"pid": property_id})
    else:
        res = db.execute(q)
    preds = [dict(r) for r in res]
    return {"predictions": preds}