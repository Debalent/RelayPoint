"""Seed script to create synthetic historical data, train a forecasting model and store model/predictions in DB.

Usage: python backend/scripts/seed_forecasting_data.py
"""
from datetime import date, timedelta
import pandas as pd
from app.services import forecasting
from app.db import SessionLocal
from app.crud import forecasting as crud


def generate_rows(days=120):
    today = date.today()
    rows = []
    for i in range(days):
        d = today - timedelta(days=(days - i))
        occupancy = int(50 + (i % 40) + (5 * (i % 7 == 0)))
        tasks = int(20 + (i % 10))
        staff = int(8 + (i % 6))
        rows.append({"date": d.isoformat(), "occupancy": occupancy, "tasks": tasks, "staff_count": staff})
    return rows


def run(property_id=1, role='housekeeping'):
    rows = generate_rows(180)
    df = forecasting.prepare_features(rows)
    meta, model_path = forecasting.train_lightgbm(df, target_col='staff_count')

    # persist model metadata
    with SessionLocal() as db:
        rec = crud.create_model_record(db, property_id=property_id, role=role, model_type='lightgbm', path=model_path, metadata=meta)

        # write sample predictions into predictions table
        preds = forecasting.predict(next(iter([forecasting.load_latest_model() or (None, None)])), df.tail(7).to_dict('records')) if False else forecasting.predict({'type':'rolling_mean','value':df['occupancy'].mean()}, df.tail(7).to_dict('records'))
        for p in preds:
            crud.create_prediction(db, property_id=property_id, role=role, date=p['date'], predicted=p['predicted'], lower=p.get('lower'), upper=p.get('upper'), model_id=rec.id)

    print(f"Seeded forecasting data, trained model saved at {model_path}")


if __name__ == '__main__':
    run()