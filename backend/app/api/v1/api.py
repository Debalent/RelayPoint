# backend/app/api/v1/api.py

from fastapi import APIRouter

# import each router from your endpoints package
from .endpoints import auth, users, teams, projects, workflows, steps, forecast, admin_forecast
from . import hospitality

api_router = APIRouter()

# existing auth & users
api_router.include_router(auth.router,     prefix="/auth",     tags=["auth"])
api_router.include_router(users.router,    prefix="/users",    tags=["users"])

# new domain routers
api_router.include_router(teams.router,    prefix="/teams",    tags=["teams"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(workflows.router,prefix="/workflows",tags=["workflows"])
api_router.include_router(steps.router,    prefix="/steps",    tags=["steps"])
# Forecasting endpoint (MVP)
api_router.include_router(forecast.router,  prefix="/forecast", tags=["forecast"])

# admin forecasting endpoints
api_router.include_router(admin_forecast.router, prefix='/admin/forecast', tags=['forecast-admin'])

# hospitality-specific operations
api_router.include_router(hospitality.router, tags=["hospitality"])

# cloudbeds integration admin endpoints
from .endpoints import cloudbeds_admin
api_router.include_router(cloudbeds_admin.router, prefix='/integrations/cloudbeds', tags=['cloudbeds-admin'])
