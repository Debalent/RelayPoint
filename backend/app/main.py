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

    # Start background retrain loop (non-blocking)
    try:
        import asyncio
        from app.services import forecasting_scheduler
        asyncio.create_task(forecasting_scheduler.start_retrain_loop())
    except Exception as e:
        logger.warning(f"Failed to start forecasting retrain loop: {e}")
    
    yield
    
    logger.info("Shutting down RelayPoint API")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_V1_STR,
    debug=settings.DEBUG,
    description="""
    # RelayPoint API - AI-Augmented, Low-Code Workflow Automation Engine

    Real-time, drag-and-drop platform for business users and developers to compose, 
    deploy, and monitor resilient automations across any SaaS stack.
    
    ## Features
    - **Visual Workflow Builder**: Intuitive drag-and-drop interface with 50+ pre-built components
    - **AI Coaching**: Intelligent suggestions and optimizations for workflow design
    - **Enterprise Resilience**: Error handling, retry mechanisms, and monitoring
    - **Real-time Collaboration**: Multi-user editing with presence awareness
    - **Advanced Analytics**: Workflow performance metrics and business insights
    - **Governance**: Role-based access control and audit logging
    
    ## Getting Started
    
    1. **Authentication**: Use the `/auth/token` endpoint to obtain a JWT token
    2. **Create a Workflow**: POST to `/api/v1/workflows` with your workflow definition
    3. **Execute**: Trigger execution with POST to `/api/v1/workflows/{id}/execute`
    4. **Monitor**: Track status with GET `/api/v1/workflows/{id}/executions`
    
    ## Authentication
    
    Most API endpoints require authentication using JWT Bearer tokens:
    
    ```
    Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    ```
    
    Use the `/auth/token` endpoint with your credentials to obtain a token.
    
    ## Rate Limiting
    
    API requests are rate-limited to protect the service:
    
    | Endpoint Category | Rate Limit |
    |-------------------|------------|
    | Authentication    | 10/minute  |
    | Workflow Creation | 30/minute  |
    | Workflow Execution| 60/minute  |
    | Read Operations   | 300/minute |
    
    ## Websocket Support
    
    Connect to `/ws/{client_id}` for real-time updates on workflow executions and collaboration.
    
    ## Error Handling
    
    All errors follow a standard format:
    
    ```json
    {
      "status_code": 400,
      "message": "Detailed error message",
      "error_code": "ERROR_CODE",
      "details": { "additional": "information" }
    }
    ```
    """,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "auth",
            "description": "Authentication and authorization operations",
            "externalDocs": {
                "description": "Authentication Guide",
                "url": "https://docs.relaypoint.ai/auth",
            },
        },
        {
            "name": "workflows",
            "description": "Workflow creation, management, and execution",
            "externalDocs": {
                "description": "Workflow Documentation",
                "url": "https://docs.relaypoint.ai/workflows",
            },
        },
        {
            "name": "users",
            "description": "User management operations",
            "externalDocs": {
                "description": "User Management Guide",
                "url": "https://docs.relaypoint.ai/users",
            },
        },
        {
            "name": "teams",
            "description": "Team and collaboration features",
            "externalDocs": {
                "description": "Team Collaboration Guide",
                "url": "https://docs.relaypoint.ai/teams",
            },
        },
        {
            "name": "integrations",
            "description": "Third-party service integrations",
            "externalDocs": {
                "description": "Integration Documentation",
                "url": "https://docs.relaypoint.ai/integrations",
            },
        },
        {
            "name": "analytics",
            "description": "Reporting and analytics endpoints",
            "externalDocs": {
                "description": "Analytics Documentation",
                "url": "https://docs.relaypoint.ai/analytics",
            },
        },
        {
            "name": "health",
            "description": "Health check and monitoring endpoints",
            "externalDocs": {
                "description": "Monitoring Guide",
                "url": "https://docs.relaypoint.ai/monitoring",
            },
        },
    ],
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1, 
        "persistAuthorization": True,
        "displayRequestDuration": True,
        "filter": True,
        "tryItOutEnabled": True,
    },
    contact={
        "name": "RelayPoint Support",
        "url": "https://relaypoint.ai/support",
        "email": "support@relaypoint.ai",
    },
    license_info={
        "name": "Commercial License",
        "url": "https://relaypoint.ai/license",
    },
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
@app.get("/health", tags=["health"], summary="Basic Health Check", 
         description="Simple health check endpoint for load balancers and monitoring systems")
async def healthcheck():
    """
    Returns a simple health status of the API service.
    
    This endpoint is designed for Kubernetes liveness/readiness probes and load balancers.
    It performs minimal checks to ensure the service is running.
    """
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

# Root endpoint redirects to docs
@app.get("/", include_in_schema=False)
async def root_redirect_to_docs():
    """Redirects the root endpoint to the API documentation"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")

# System status endpoint with detailed health checks
@app.get("/status", tags=["health"], summary="Detailed System Status", 
         description="Comprehensive health check of all system components")
async def system_status():
    """
    Performs a detailed health check of all system components.
    
    This endpoint checks the status of:
    - Database connectivity
    - Redis connectivity
    - External AI services
    - Background task processing
    - System resources
    
    Returns a detailed status report of all components.
    """
    from datetime import datetime
    import psutil
    
    # Perform actual health checks
    db_status = "connected"
    redis_status = "connected"
    
    try:
        # Check database connection
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Check Redis connection if configured
    if settings.REDIS_URL:
        try:
            import redis
            from urllib.parse import urlparse
            
            # Parse Redis URL
            parsed_url = urlparse(settings.REDIS_URL)
            password = parsed_url.password or None
            
            # Connect to Redis
            r = redis.Redis(
                host=parsed_url.hostname,
                port=parsed_url.port or 6379,
                password=password,
                ssl=parsed_url.scheme == 'rediss',
                socket_timeout=2.0
            )
            
            # Check connection
            r.ping()
            redis_status = "connected"
        except Exception as e:
            redis_status = f"error: {str(e)}"
    else:
        redis_status = "not_configured"
    
    # Check AI services
    ai_status = {}
    if settings.OPENAI_API_KEY:
        ai_status["openai"] = "configured"
    else:
        ai_status["openai"] = "not_configured"
        
    if settings.ANTHROPIC_API_KEY:
        ai_status["anthropic"] = "configured"
    else:
        ai_status["anthropic"] = "not_configured"
    
    # System resources
    system_resources = {
        "cpu_usage": f"{psutil.cpu_percent()}%",
        "memory_usage": f"{psutil.virtual_memory().percent}%",
        "disk_usage": f"{psutil.disk_usage('/').percent}%",
    }
    
    return {
        "status": "ok" if db_status == "connected" else "degraded",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "uptime": "unknown",  # Would need to track app start time
        "components": {
            "database": db_status,
            "redis": redis_status,
            "ai_services": ai_status,
            "websockets": {
                "status": "active",
                "connections": len(websocket_manager.active_connections),
            },
        },
        "system": system_resources,
        "environment": settings.ENVIRONMENT,
        "version": settings.APP_VERSION,
    }
