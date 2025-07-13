```python
"""
FastAPI endpoints for managing users in RelayPoint.

This module defines API endpoints for creating, reading, updating, and deleting users,
who interact with teams and projects in RelayPoint's AI-augmented, low-code workflow
automation engine. Users are authenticated via Auth0 and linked to teams, with operations
logged for audit trails and observability, supporting enterprise-grade features like
resilience and compliance.

WHY IT MATTERS FOR INVESTORS:
- Scalability: Integrates with PostgreSQL and TimescaleDB for high-throughput storage of
  user, team, and workflow data, supporting enterprise workloads.
- Reliability: Robust error handling, audit trails, and rollback support ensure consistent
  operations, aligning with enterprise SLAs.
- Compliance: Audit-ready user operations meet GDPR, HIPAA, and SOC 2 requirements,
  appealing to regulated industries like finance and healthcare.
- Developer Productivity: Type-safe endpoints and AI-driven insights (via Grok 3 or
  Llama 3.1) streamline development, reducing time-to-market.
- Market Alignment: Supports RelayPoint's core value proposition of low-code automation
  with AI augmentation, targeting a $140.80B agentic AI market by 2032 (39.3% CAGR).

@since Initial commit (User endpoints for RelayPoint backend)
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from prometheus_client import Counter, Histogram
from loguru import logger
import app.crud.user as crud
import app.schemas.user as schemas
from app.db.session import get_async_db
from app.auth.auth0 import verify_auth0_token, get_current_user
from app.models import User, Team, WorkflowRun
from app.ai.workflow_coach import suggest_user_insights

# Prometheus metrics for observability
user_requests = Counter("relaypoint_user_requests_total", "Total user requests", ["endpoint", "method"])
user_latency = Histogram("relaypoint_user_request_latency_seconds", "User request latency", ["endpoint"])
audit_trail_logs = Counter("relaypoint_user_audit_trails_total", "Total audit trail logs", ["operation"])

# OAuth2 configuration for Auth0
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="https://<your-auth0-domain>/oauth/token")

# FastAPI router for user endpoints
router = APIRouter(prefix="/users", tags=["users"])

async def log_audit_trail(
    db: AsyncSession,
    user_id: str,
    operation: str,
    auth_user_id: str,
    metadata: Optional[dict] = None
) -> None:
    """
    Logs an audit trail for user operations to TimescaleDB.

    Args:
        db: Async database session.
        user_id: UUID of the user.
        operation: Operation performed (e.g., 'create', 'delete').
        auth_user_id: ID of the authenticated user performing the operation.
        metadata: Optional additional metadata.

    Raises:
        sa.exc.SQLAlchemyError: If the audit trail fails to save.
    """
    try:
        audit_trail = WorkflowRun(
            workflow_id=None,  # User-level audit, not tied to a specific workflow
            timestamp=func.now(),
            status=operation,
            metadata={"user_id": user_id, "auth_user_id": auth_user_id, **(metadata or {})}
        )
        db.add(audit_trail)
        await db.commit()
        audit_trail_logs.labels(operation=operation).inc()
        logger.info(f"Audit trail logged for user {user_id}: {operation}")
    except sa.exc.SQLAlchemyError as e:
        logger.error(f"Failed to log audit trail: {str(e)}")
        raise

@router.post(
    "/",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
async def register_user(
    user_in: schemas.UserCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Security(get_current_user, scopes=["write:users"])
):
    """
    Register a new user with audit trail logging.

    Args:
        user_in: User creation data (phone, name, etc.).
        db: Async database session.
        current_user: Authenticated user from Auth0 (admin scope).

    Returns:
        schemas.UserRead: Created user details.

    Raises:
        HTTPException: If the phone is already registered (400) or an error occurs (500).
    """
    with user_latency.labels(endpoint="/users").time():
        user_requests.labels(endpoint="/users", method="POST").inc()
        try:
            if await crud.get_user_by_phone(db, user_in.phone):
                raise HTTPException(status_code=400, detail="Phone already registered")
            user = await crud.create_user(db, user_in)
            await log_audit_trail(db, str(user.id), "create", current_user["sub"], {"phone": user_in.phone, "name": user_in.name})
            return user
        except sa.exc.SQLAlchemyError as e:
            logger.error(f"User registration failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/",
    response_model=List[schemas.UserRead],
    summary="List users"
)
async def read_users(
    skip: int = 0,
    limit: int = 100,
    team_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Security(get_current_user, scopes=["read:users"])
):
    """
    Retrieve a list of users, optionally filtered by team_id.

    Args:
        skip: Number of users to skip (pagination).
        limit: Maximum number of users to return.
        team_id: Optional UUID to filter users by team membership.
        db: Async database session.
        current_user: Authenticated user from Auth0.

    Returns:
        List[schemas.UserRead]: List of user details.

    Raises:
        HTTPException: If the team_id is invalid (400) or an error occurs (500).
    """
    with user_latency.labels(endpoint="/users").time():
        user_requests.labels(endpoint="/users", method="GET").inc()
        try:
            if team_id:
                team = await db.execute(select(Team).filter_by(id=str(team_id)))
                if not team.scalars().first():
                    raise HTTPException(status_code=400, detail="Invalid team_id")
                users = await crud.get_users_by_team(db, str(team_id), skip, limit)
            else:
                users = await crud.get_users(db, skip, limit)
            await log_audit_trail(db, "all", "list", current_user["sub"], {"skip": skip, "limit": limit, "team_id": str(team_id) if team_id else None})
            return users
        except sa.exc.SQLAlchemyError as e:
            logger.error(f"User listing failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/{user_id}",
    response_model=schemas.UserRead,
    summary="Get a user by ID"
)
async def read_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Security(get_current_user, scopes=["read:users"])
):
    """
    Retrieve a user by their UUID.

    Args:
        user_id: UUID of the user.
        db: Async database session.
        current_user: Authenticated user from Auth0.

    Returns:
        schemas.UserRead: User details.

    Raises:
        HTTPException: If the user is not found (404) or an error occurs (500).
    """
    with user_latency.labels(endpoint="/users/{user_id}").time():
        user_requests.labels(endpoint="/users/{user_id}", method="GET").inc()
        try:
            user = await crud.get_user(db, str(user_id))
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            await log_audit_trail(db, str(user_id), "read", current_user["sub"])
            return user
        except sa.exc.SQLAlchemyError as e:
            logger.error(f"User retrieval failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.put(
    "/{user_id}",
    response_model=schemas.UserRead,
    summary="Update a user"
)
async def update_user(
    user_id: UUID,
    user_in: schemas.UserUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Security(get_current_user, scopes=["write:users"])
):
    """
    Update a user by their UUID.

    Args:
        user_id: UUID of the user.
        user_in: User update data (e.g., name, phone).
        db: Async database session.
        current_user: Authenticated user from Auth0.

    Returns:
        schemas.UserRead: Updated user details.

    Raises:
        HTTPException: If the user is not found (404), phone is taken (400), or an error occurs (500).
    """
    with user_latency.labels(endpoint="/users/{user_id}").time():
        user_requests.labels(endpoint="/users/{user_id}", method="PUT").inc()
        try:
            user = await crud.get_user(db, str(user_id))
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            if user_in.phone and user_in.phone != user.phone and await crud.get_user_by_phone(db, user_in.phone):
                raise HTTPException(status_code=400, detail="Phone already registered")
            updated_user = await crud.update_user(db, str(user_id), user_in)
            await log_audit_trail(db, str(user_id), "update", current_user["sub"], {"updates": user_in.dict(exclude_unset=True)})
            return updated_user
        except sa.exc.SQLAlchemyError as e:
            logger.error(f"User update failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user"
)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Security(get_current_user, scopes=["write:users"])
):
    """
    Delete a user by their UUID.

    Args:
        user_id: UUID of the user.
        db: Async database session.
        current_user: Authenticated user from Auth0.

    Raises:
        HTTPException: If the user is not found (404) or an error occurs (500).
    """
    with user_latency.labels(endpoint="/users/{user_id}").time():
        user_requests.labels(endpoint="/users/{user_id}", method="DELETE").inc()
        try:
            success = await crud.delete_user(db, str(user_id))
            if not success:
                raise HTTPException(status_code=404, detail="User not found")
            await log_audit_trail(db, str(user_id), "delete", current_user["sub"])
        except sa.exc.SQLAlchemyError as e:
            logger.error(f"User deletion failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.post(
    "/{user_id}/insights",
    response_model=schemas.UserInsightsResponse,
    summary="Get AI-driven user insights"
)
async def get_user_insights(
    user_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Security(get_current_user, scopes=["read:users", "write:users"])
):
    """
    Retrieve AI-driven insights for a user based on their project and workflow activity.

    Uses Grok 3 or Llama 3.1 to analyze user interactions with projects and workflows,
    providing insights like activity levels or workflow contribution patterns.

    Args:
        user_id: UUID of the user.
        db: Async database session.
        current_user: Authenticated user from Auth0.

    Returns:
        schemas.UserInsightsResponse: AI-generated user insights.

    Raises:
        HTTPException: If the user is not found (404) or AI processing fails (500).
    """
    with user_latency.labels(endpoint="/users/{user_id}/insights").time():
        user_requests.labels(endpoint="/users/{user_id}/insights", method="POST").inc()
        try:
            user = await crud.get_user(db, str(user_id))
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            # Fetch user-related workflow run data
            runs = await db.execute(
                select(WorkflowRun)
                .filter(WorkflowRun.metadata["user_id"].astext == str(user_id))
                .limit(100)
            )
            run_data = [run.metadata for run in runs.scalars().all()]
            insights = await suggest_user_insights(user.phone, run_data)
            await log_audit_trail(db, str(user_id), "insights", current_user["sub"], {"insights": insights})
            return schemas.UserInsightsResponse(insights=insights)
        except Exception as e:
            logger.error(f"User insights failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
```
