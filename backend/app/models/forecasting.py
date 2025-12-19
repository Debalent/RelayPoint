from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, ForeignKey
from sqlalchemy.sql import func
from app.models.base import Base

class ForecastModel(Base):
    __tablename__ = "forecast_models"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, nullable=False)
    role = Column(String, nullable=False)
    model_type = Column(String, nullable=False)
    version = Column(String, nullable=True)
    metadata = Column(JSON, nullable=True)
    path = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class ForecastPrediction(Base):
    __tablename__ = "forecast_predictions"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, nullable=False)
    role = Column(String, nullable=False)
    date = Column(String, nullable=False)
    predicted = Column(Float, nullable=False)
    lower = Column(Float, nullable=True)
    upper = Column(Float, nullable=True)
    model_id = Column(Integer, ForeignKey("forecast_models.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class ForecastOverride(Base):
    __tablename__ = "forecast_overrides"

    id = Column(Integer, primary_key=True, index=True)
    property_id = Column(Integer, nullable=False)
    role = Column(String, nullable=False)
    date = Column(String, nullable=False)
    override_value = Column(Float, nullable=False)
    reason = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())