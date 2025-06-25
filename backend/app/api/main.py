from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.api import api_router
from app.db import Base, engine

# Create DB tables on startup (dev only – use Alembic in prod)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    openapi_prefix=settings.API_V1_STR,
)

# Mount v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok"}
