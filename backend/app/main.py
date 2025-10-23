# backend/app/main.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import structlog
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from prometheus_client import make_asgi_app

from app.core.config import settings
from app.api.v1.api import router as api_v1_router
from app.core.websocket_manager import WebSocketManager
from app.core.database import engine
from app.models import Base

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Initialize Sentry for error tracking
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        integrations=[FastApiIntegration(auto_enable=True)],
        traces_sample_rate=1.0,
        environment=settings.ENVIRONMENT,
    )

# WebSocket manager for real-time features
websocket_manager = WebSocketManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting RelayPoint API", version=settings.APP_VERSION)
    
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    logger.info("Shutting down RelayPoint API")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_V1_STR,
    debug=settings.DEBUG,
    description="""
    RelayPoint API - AI-Augmented, Low-Code Workflow Automation Engine
    
    Real-time, drag-and-drop platform for business users and developers to compose, 
    deploy, and monitor resilient automations across any SaaS stack.
    
    Features:
    - Visual workflow builder with AI coaching
    - Enterprise-grade resilience and monitoring
    - Real-time collaboration and notifications
    - Advanced analytics and governance
    """,
    lifespan=lifespan,
)

# Add security middleware
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our v1 routes under /api/v1
app.include_router(api_v1_router, prefix=settings.API_V1_STR)

# Add Prometheus metrics endpoint
if settings.PROMETHEUS_ENABLED:
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)

# WebSocket endpoint for real-time features
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket_manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket_manager.send_personal_message(f"Echo: {data}", client_id)
    except WebSocketDisconnect:
        websocket_manager.disconnect(client_id)

# Enhanced health check with system status
@app.get("/", tags=["health"])
async def healthcheck():
    return {
        "status": "ok", 
        "service": settings.PROJECT_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "features": {
            "ai_enabled": bool(settings.OPENAI_API_KEY),
            "redis_enabled": bool(settings.REDIS_URL),
            "websockets_enabled": True,
            "prometheus_enabled": settings.PROMETHEUS_ENABLED,
        }
    }

# System status endpoint
@app.get("/status", tags=["health"])
async def system_status():
    """Detailed system status for monitoring"""
    return {
        "database": "connected",  # Add actual DB health check
        "redis": "connected",     # Add actual Redis health check
        "ai_services": "available",
        "timestamp": "2025-10-22T00:00:00Z",
    }
