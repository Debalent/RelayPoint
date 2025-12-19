from sqlalchemy.orm import Session
from app.models import forecasting as fmodels


def create_override(db: Session, *, property_id: int, role: str, date: str, override_value: float, reason: str = None):
    obj = fmodels.ForecastOverride(property_id=property_id, role=role, date=date, override_value=override_value, reason=reason)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def create_model_record(db: Session, *, property_id: int, role: str, model_type: str, path: str, metadata: dict = None, version: str = None):
    obj = fmodels.ForecastModel(property_id=property_id, role=role, model_type=model_type, path=path, metadata=metadata or {}, version=version)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def create_prediction(db: Session, *, property_id: int, role: str, date: str, predicted: float, lower: float = None, upper: float = None, model_id: int = None):
    obj = fmodels.ForecastPrediction(property_id=property_id, role=role, date=date, predicted=predicted, lower=lower, upper=upper, model_id=model_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
