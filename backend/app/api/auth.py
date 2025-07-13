```python
"""
FastAPI endpoints for user authentication in RelayPoint.

This module defines API endpoints for user registration, login, token refresh, and
authentication insights, using Auth0 for secure OAuth 2.0-based authentication in
RelayPoint's AI-augmented, low-code workflow automation engine. Authentication events
are logged to TimescaleDB for audit trails, supporting enterprise-grade security,
observability, and compliance.

WHY IT MATTERS FOR INVESTORS:
- Security: Auth0 integration ensures industry-standard OAuth 2.0 authentication with
  RBAC, protecting sensitive workflow and project data.
- Scalability: Async FastAPI and TimescaleDB handle high-throughput authentication
  requests, supporting enterprise workloads.
- Reliability: Robust error handling and audit trails ensure consistent operations,
  aligning with enterprise SLAs.
- Compliance: Audit-ready authentication logs meet GDPR, HIPAA, and SOC 2 requirements,
  appealing to regulated industries like finance and healthcare.
- Developer Productivity: Type-safe endpoints and AI-driven insights (via Grok 3 or
  Llama 3.1) streamline development, reducing time-to-market.
- Market Alignment: Supports RelayPoint's core value proposition of low-code automation
  with AI augmentation, targeting a $140.80B agentic AI market by 2032 (39.3% CAGR).

@since Initial commit (Auth endpoints for RelayPoint backend)
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from prometheus_client import Counter, Histogram
from loguru import logger
from jose import jwt, JWTError
from datetime import datetime, timedelta
import httpx
import app.crud.user as crud
import app.schemas.user as schemas
from app.db.session import get_async_db
from app.models import User, WorkflowRun
from app.ai.workflow_coach import suggest_auth_insights

# Configuration (move to core/settings.py in production)
AUTH0_DOMAIN = "<your-auth0-domain>"
AUTH0_AUDIENCE = "<your-auth0-audience>"
AUTH0_ISSUER = f"https://{AUTH0_DOMAIN}/"
JWT_ALGORITHM = "RS256"

# Prometheus metrics for observability
auth_requests = Counter("relaypoint_auth_requests_total", "Total auth requests", ["endpoint", "method"])
auth_latency = Histogram("relaypoint_auth_request_latency_seconds", "Auth request latency", ["endpoint"])
audit_trail_logs = Counter("relaypoint_auth_audit_trails_total", "Total audit trail logs", ["operation"])

# OAuth2 configuration for Auth0
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"https://{AUTH0_DOMAIN}/oauth/token")

# FastAPI router for auth endpoints
router = APIRouter(prefix="/auth", tags=["auth"])

async def verify_auth0_token(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Verify an Auth0 JWT token.

    Args:
        token: JWT token from Auth0.

    Returns:
        dict: Decoded token payload.

    Raises:
        HTTPException: If the token is invalid or verification fails.
    """
    try:
        async with httpx.AsyncClient() as client:
            jwks = await client.get(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
            jwks = jwks.json()
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if not rsa_key:
            raise HTTPException(status_code=401, detail="Invalid token: No matching JWKS key")
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=[JWT_ALGORITHM],
            audience=AUTH0_AUDIENCE,
            issuer=AUTH0_ISSUER
        )
        return payload
    except JWTError as e:
        logger.error(f"Token verification failed: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Get the current user from an Auth0 token.

    Args:
        token: JWT token from Auth0.

    Returns:
        dict: User payload with 'sub' (user ID) and scopes.

    Raises:
        HTTPException: If the token is invalid.
    """
    return await verify_auth0_token(token)

async def log_audit_trail(
    db: AsyncSession,
    user_id: str,
    operation: str,
    metadata: Optional[dict] = None
) -> None:
    """
    Logs an audit trail for authentication operations to TimescaleDB.

    Args:
        db: Async database session.
        user_id: UUID of the user.
        operation: Operation performed (e.g., 'register', 'login').
        metadata: Optional additional metadata.

    Raises:
        sa.exc.SQLAlchemyError: If the audit trail fails to save.
    """
    try:
        audit_trail = WorkflowRun(
            workflow_id=None,  # Auth-level audit, not tied to a specific workflow
            timestamp=func.now(),
            status=operation,
            metadata={"user_id": user_id, **(metadata or {})}
        )
        db.add(audit_trail)
        await db.commit()
        audit_trail_logs.labels(operation=operation).inc()
        logger.info(f"Audit trail logged for user {user_id}: {operation}")
    except sa.exc.SQLAlchemyError as e:
        logger.error(f"Failed to log audit trail: {str(e)}")
        raise

@router.post(
    "/register",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user via Auth0"
)
async def register_user(
    user_in: schemas.UserCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Security(get_current_user, scopes=["write:users"])
):
    """
    Register a new user with Auth0 and store in the database.

    Args:
        user_in: User creation data (phone, name).
        db: Async database session.
        current_user: Authenticated admin user from Auth0.

    Returns:
        schemas.UserRead: Created user details.

    Raises:
        HTTPException: If the phone is already registered (400) or an error occurs (500).
    """
    with auth_latency.labels(endpoint="/auth/register").time():
        auth_requests.labels(endpoint="/auth/register", method="POST").inc()
        try:
            if await crud.get_user_by_phone(db, user_in.phone):
                raise HTTPException(status_code=400, detail="Phone already registered")
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://{AUTH0_DOMAIN}/dbconnections/signup",
                    json={
                        "client_id": "<your-auth0-client-id>",
                        "connection": "Username-Password-Authentication",
                        "email": user_in.email,  # Assuming email added to schema
                        "password": user_in.password,
                        "name": user_in.name
                    }
                )
                if response.status_code != 200:
                    raise HTTPException(status_code=400, detail="Auth0 registration failed")
                auth0_user = response.json()
            user = await crud.create_user(db, user_in, auth0_user_id=auth0_user["_id"])
            await log_audit_trail(db, str(user.id), "register", {"phone": user_in.phone, "name": user_in.name})
            return user
        except sa.exc.SQLAlchemyError as e:
            logger.error(f"User registration failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.post(
    "/login",
    response_model=schemas.Token,
    summary="Log in a user via Auth0"
)
async def login_user(
    data: schemas.UserLogin,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Log in a user via Auth0 and return an access token.

    Args:
        data: User login data (email, password).
        db: Async database session.

    Returns:
        schemas.Token: Access token and token type.

    Raises:
        HTTPException: If credentials are invalid (401) or an error occurs (500).
    """
    with auth_latency.labels(endpoint="/auth/login").time():
        auth_requests.labels(endpoint="/auth/login", method="POST").inc()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://{AUTH0_DOMAIN}/oauth/token",
                    json={
                        "client_id": "<your-auth0-client-id>",
                        "client_secret": "<your-auth0-client-secret>",
                        "audience": AUTH0_AUDIENCE,
                        "grant_type": "password",
                        "username": data.email,
                        "password": data.password,
                        "scope": "openid profile email read:users write:users read:teams write:teams read:projects write:projects"
                    }
                )
                if response.status_code != 200:
                    raise HTTPException(status_code=401, detail="Invalid credentials")
                token_data = response.json()
            user = await crud.get_user_by_email(db, data.email)
            if not user:
                raise HTTPException(status_code=401, detail="User not found in database")
            await log_audit_trail(db, str(user.id), "login", {"email": data.email})
            return {"access_token": token_data["access_token"], "token_type": token_data["token_type"]}
        except sa.exc.SQLAlchemyError as e:
            logger.error(f"Login failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.post(
    "/refresh",
    response_model=schemas.Token,
    summary="Refresh an Auth0 access token"
)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Refresh an Auth0 access token using a refresh token.

    Args:
        refresh_token: Refresh token from Auth0.
        db: Async database session.

    Returns:
        schemas.Token: New access token and token type.

    Raises:
        HTTPException: If the refresh token is invalid (401) or an error occurs (500).
    """
    with auth_latency.labels(endpoint="/auth/refresh").time():
        auth_requests.labels(endpoint="/auth/refresh", method="POST").inc()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://{AUTH0_DOMAIN}/oauth/token",
                    json={
                        "client_id": "<your-auth0-client-id>",
                        "client_secret": "<your-auth0-client-secret>",
                        "grant_type": "refresh_token",
                        "refresh_token": refresh_token
                    }
                )
                if response.status_code != 200:
                    raise HTTPException(status_code=401, detail="Invalid refresh token")
                token_data = response.json()
            # Log refresh event (user_id may not be available without token introspection)
            await log_audit_trail(db, "unknown", "refresh", {"refresh_token": refresh_token[:10] + "..."})
            return {"access_token": token_data["access_token"], "token_type": token_data["token_type"]}
        except Exception as e:
            logger.error(f"Token refresh failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.post(
    "/insights",
    response_model=schemas.AuthInsightsResponse,
    summary="Get AI-driven authentication insights"
)
async def get_auth_insights(
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Security(get_current_user, scopes=["read:users", "write:users"])
):
    """
    Retrieve AI-driven insights for authentication patterns.

    Uses Grok 3 or Llama 3.1 to analyze authentication events (e.g., login frequency,
    suspicious patterns) based on audit trails in TimescaleDB.

    Args:
        db: Async database session.
        current_user: Authenticated admin user from Auth0.

    Returns:
        schemas.AuthInsightsResponse: AI-generated authentication insights.

    Raises:
        HTTPException: If AI processing fails (500).
    """
    with auth_latency.labels(endpoint="/auth/insights").time():
        auth_requests.labels(endpoint="/auth/insights", method="POST").inc()
        try:
            # Fetch recent authentication audit trails
            runs = await db.execute(
                select(WorkflowRun)
                .filter(WorkflowRun.status.in_(["login", "register", "refresh"]))
                .limit(100)
            )
            run_data = [run.metadata for run in runs.scalars().all()]
            insights = await suggest_auth_insights(run_data)
            await log_audit_trail(db, current_user["sub"], "insights", {"insights": insights})
            return schemas.AuthInsightsResponse(insights=insights)
        except Exception as e:
            logger.error(f"Auth insights failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
```
