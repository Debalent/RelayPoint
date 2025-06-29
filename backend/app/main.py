# backend/app/main.py

from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.api import router as api_v1_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_V1_STR,
    debug=settings.DEBUG,
)

# include our v1 routes under /api/v1
app.include_router(api_v1_router, prefix=settings.API_V1_STR)

# optionally: root healthcheck
@app.get("/", tags=["health"])
def healthcheck():
    return {"status": "ok", "service": settings.PROJECT_NAME}
