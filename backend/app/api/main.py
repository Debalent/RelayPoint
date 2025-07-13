```python
"""
Main FastAPI application for RelayPoint.

This module serves as the entry point for RelayPoint's AI-augmented, low-code workflow
automation engine, initializing the FastAPI app, mounting API routers, and setting up
database connections, observability, and security. It supports enterprise-grade features
like scalability, reliability, and compliance, with integration for Auth0, Prometheus,
Loki, and TimescaleDB.

WHY IT MATTERS FOR INVESTORS:
- Scalability: Async FastAPI and TimescaleDB handle high-throughput workloads for
  enterprise-grade workflows, projects, teams, and users.
- Reliability: Global exception handling, audit trails, and startup/shutdown hooks ensure
  consistent operations, aligning with enterprise SLAs.
- Compliance: Audit-ready logging in TimescaleDB meets GDPR, HIPAA, and SOC 2 requirements,
  appealing to regulated industries like finance and healthcare.
- Security: Auth0 integration provides industry-standard OAuth 2.0 authentication with RBAC.
- Developer Productivity: Type-safe code and AI-driven features (via Grok 3 or Llama 3.1)
  streamline development, reducing time-to-market.
- Market Alignment: Supports RelayPoint's core value proposition of low-code automation
  with AI augmentation, targeting a $140.80B agentic AI market by 2032 (39.3% CAGR).

@since Initial commit (Main FastAPI application for RelayPoint backend)
"""

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app, Counter, Histogram
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
import app.core.config as config
from app.api.v1.api import api_router
from app.db.session import get_async_db, engine
from app.db import Base
from app.models import WorkflowRun
from sqlalchemy.sql import func
import httpx
import time

# Prometheus metrics for observability
api_requests = Counter("relaypoint_api_requests_total", "Total API requests", ["endpoint", "method"])
api_latency = Histogram("relaypoint_api_request_latency_seconds", "API request latency", ["endpoint"])
audit_trail_logs = Counter("relaypoint_api_audit_trails_total", "Total audit trail logs", ["operation"])

# Configuration
settings = config.Settings()

# Startup/shutdown hooks
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage startup and shutdown events for the FastAPI application.

    Initializes database connections, Prometheus metrics, and logs startup events.
    Cleans up resources on shutdown.

    Args:
        app: FastAPI application instance.
    """
    # Startup
    logger.info("Starting RelayPoint FastAPI application")
    async with engine.begin() as conn:
        # Create tables if not using Alembic (dev only)
        if settings.DEBUG:
            await conn.run_sync(Base.metadata.create_all)
    async with httpx.AsyncClient() as client:
        logger.info("Initialized HTTP client for Auth0 and external services")
    
    # Log startup audit trail
    async with get_async_db() as db:
        try:
            audit_trail = WorkflowRun(
                workflow_id=None,
                timestamp=func.now(),
                status="startup",
                metadata={"app": "relaypoint", "version": settings.APP_VERSION}
            )
            db.add(audit_trail)
            await db.commit()
            audit_trail_logs.labels(operation="startup").inc()
        except Exception as e:
            logger.error(f"Failed to log startup audit trail: {str(e)}")
    
    yield  # Run application

    # Shutdown
    logger.info("Shutting down RelayPoint FastAPI application")
    async with get_async_db() as db:
        try:
            audit_trail = WorkflowRun(
                workflow_id=None,
                timestamp=func.now(),
                status="shutdown",
                metadata={"app": "relaypoint", "version": settings.APP_VERSION}
            )
            db.add(audit_trail)
            await db.commit()
            audit_trail_logs.labels(operation="shutdown").inc()
        except Exception as e:
            logger.error(f"Failed to log shutdown audit trail: {str(e)}")
    await engine.dispose()

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="RelayPoint: AI-augmented, low-code workflow automation engine",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Prometheus metrics endpoint
app.mount("/metrics", make_asgi_app())

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handle HTTP exceptions globally with audit trail logging.

    Args:
        request: Incoming HTTP request.
        exc: HTTPException raised.

    Returns:
        JSONResponse: Error response with details.
    """
    api_requests.labels(endpoint=str(request.url.path), method=request.method).inc()
    async with get_async_db() as db:
        try:
            audit_trail = WorkflowRun(
                workflow_id=None,
                timestamp=func.now(),
                status="error",
                metadata={
                    "endpoint": str(request.url.path),
                    "method": request.method,
                    "status_code": exc.status_code,
                    "detail": exc.detail
                }
            )
            db.add(audit_trail)
            await db.commit()
            audit_trail_logs.labels(operation="error").inc()
        except Exception as e:
            logger.error(f"Failed to log error audit trail: {str(e)}")
    logger.error(f"HTTP error: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle uncaught exceptions globally with audit trail logging.

    Args:
        request: Incoming HTTP request.
        exc: Exception raised.

    Returns:
        JSONResponse: Error response with generic message.
    """
    api_requests.labels(endpoint=str(request.url.path), method=request.method).inc()
    async with get_async_db() as db:
        try:
            audit_trail = WorkflowRun(
                workflow_id=None,
                timestamp=func.now(),
                status="error",
                metadata={
                    "endpoint": str(request.url.path),
                    "method": request.method,
                    "error": str(exc)
                }
            )
            db.add(audit_trail)
            await db.commit()
            audit_trail_logs.labels(operation="error").inc()
        except Exception as e:
            logger.error(f"Failed to log error audit trail: {str(e)}")
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

# Mount v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["health"])
async def health_check():
    """
    Health check endpoint for the RelayPoint API.

    Returns:
        dict: Status of the API.
    """
    with api_latency.labels(endpoint="/").time():
        api_requests.labels(endpoint="/", method="GET").inc()
        return {"status": "ok", "version": settings.APP_VERSION}

@app.get("/health", tags=["health"])
async def detailed_health_check(db: AsyncSession = Depends(get_async_db)):
    """
    Detailed health check endpoint, verifying database connectivity.

    Args:
        db: Async database session.

    Returns:
        dict: Detailed status of the API and database.

    Raises:
        HTTPException: If database connectivity fails.
    """
    with api_latency.labels(endpoint="/health").time():
        api_requests.labels(endpoint="/health", method="GET").inc()
        try:
            # Test database connectivity
            await db.execute(select(1))
            return {
                "status": "ok",
                "version": settings.APP_VERSION,
                "database": "connected",
                "timestamp": time.time()
            }
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            raise HTTPException(status_code=503, detail="Database connectivity failed")
```
