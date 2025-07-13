```python
"""
FastAPI endpoints for managing teams in RelayPoint.

This module defines API endpoints for creating, reading, updating, and deleting teams,
which are logical groupings of users and projects in RelayPoint's AI-augmented, low-code
workflow automation engine. Teams enable collaborative workflow management and integrate
with projects, workflows, and audit trails, supporting enterprise-grade features like
resilience, observability, and AI-driven insights.

WHY IT MATTERS FOR INVESTORS:
- Scalability: Integrates with PostgreSQL and TimescaleDB for high-throughput storage of
  team, project, and workflow data, supporting enterprise workloads.
- Reliability: Robust error handling, audit trails, and rollback support ensure consistent
  operations, aligning with enterprise SLAs.
- Compliance: Audit-ready team operations meet GDPR, HIPAA, and SOC 2 requirements,
  appealing to regulated industries like finance and healthcare.
- Developer Productivity: Type-safe endpoints and AI-driven insights (via Grok 3 or
  Llama 3.1) streamline development, reducing time-to-market.
- Market Alignment: Supports RelayPoint's core value proposition of low-code automation
  with AI augmentation, targeting a $140.80B agentic AI market by 2032 (39.3% CAGR).

@since Initial commit (Team endpoints for RelayPoint backend)
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from prometheus_client import Counter, Histogram
from loguru import logger
import app.crud.team as crud
import app.schemas.team as schemas
from app.db.session import get_async_db
from app.auth.auth0 import verify_auth0_token, get_current_user
from app.models import Team, Project, WorkflowRun
from app.ai.workflow_coach import suggest_team_insights

# Prometheus metrics for observability
team_requests = Counter("relaypoint_team_requests_total", "Total team requests", ["endpoint", "method"])
team_latency = Histogram("relaypoint_team_request_latency_seconds", "Team request latency", ["endpoint"])
audit_trail_logs = Counter("relaypoint_team_audit_trails_total", "Total audit trail logs", ["operation"])

# OAuth2 configuration for Auth0
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="https://<your-auth0-domain>/oauth/token")

# FastAPI router for team endpoints
router = APIRouter(prefix="/teams", tags=["teams"])

async def log_audit_trail(
    db: AsyncSession,
    team_id: str,
    operation: str,
    user_id: str,
    metadata: Optional[dict] = None
) -> None:
    """
    Logs an audit trail for team operations to TimescaleDB.

    Args:
        db: Async database session.
        team_id: UUID of the team.
        operation: Operation performed (e.g., 'create', 'delete').
        user_id: ID of the user performing the operation.
        metadata: Optional additional metadata.

    Raises:
        sa.exc.SQLAlchemyError: If the audit trail fails to save.
    """
    try:
        audit_trail = WorkflowRun(
            workflow_id=None,  # Team-level audit, not tied to a specific workflow
            timestamp=func.now(),
            status=operation,
            metadata={"team_id": team_id, "user_id": user_id, **(metadata or {})}
        )
        db.add(audit_trail)
        await db.commit()
        audit_trail_logs.labels(operation=operation).inc()
        logger.info(f"Audit trail logged for team {team_id}: {operation}")
    except sa.exc.SQLAlchemyError as e:
        logger.error(f"Failed to log audit trail: {str(e)}")
        raise

@router.post(
    "/",
    response_model=schemas.TeamRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new team"
)
async def create_team(
    team_in: schemas.TeamCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Security(get_current_user, scopes=["write:teams"])
):
    """
    Create a new team with audit trail logging.

    Args:
        team_in: Team creation data (name, etc.).
        db: Async database session.
        current_user: Authenticated user from Auth0.

    Returns:
        schemas.TeamRead: Created team details.

    Raises:
        HTTPException: If the team creation fails (500).
    """
    with team_latency.labels(endpoint="/teams").time():
        team_requests.labels(endpoint="/teams", method="POST").inc()
        try:
            team = await crud.create_team(db, team_in)
            await log_audit_trail(db, str(team.id), "create", current_user["sub"], {"team_name": team.name})
            return team
        except sa.exc.SQLAlchemyError as e:
            logger.error(f"Team creation failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/",
    response_model=List[schemas.TeamRead],
    summary="List teams"
)
async def read_teams(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Security(get_current_user, scopes=["read:teams"])
):
    """
    Retrieve a list of teams with pagination.

    Args:
        skip: Number of teams to skip (pagination).
        limit: Maximum number of teams to return.
        db: Async database session.
        current_user: Authenticated user from Auth0.

    Returns:
        List[schemas.TeamRead]: List of team details.

    Raises:
        HTTPException: If the team listing fails (500).
    """
    with team_latency.labels(endpoint="/teams").time():
        team_requests.labels(endpoint="/teams", method="GET").inc()
        try:
            teams = await crud.get_teams(db, skip, limit)
            await log_audit_trail(db, "all", "list", current_user["sub"], {"skip": skip, "limit": limit})
            return teams
        except sa.exc.SQLAlchemyError as e:
            logger.error(f"Team listing failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/{team_id}",
    response_model=schemas.TeamRead,
    summary="Get a team by ID"
)
async def read_team(
    team_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Security(get_current_user, scopes=["read:teams"])
):
    """
    Retrieve a team by its UUID.

    Args:
        team_id: UUID of the team.
        db: Async database session.
        current_user: Authenticated user from Auth0.

    Returns:
        schemas.TeamRead: Team details.

    Raises:
        HTTPException: If the team is not found (404) or an error occurs (500).
    """
    with team_latency.labels(endpoint="/teams/{team_id}").time():
        team_requests.labels(endpoint="/teams/{team_id}", method="GET").inc()
        try:
            team = await crud.get_team(db, str(team_id))
            if not team:
                raise HTTPException(status_code=404, detail="Team not found")
            await log_audit_trail(db, str(team_id), "read", current_user["sub"])
            return team
        except sa.exc.SQLAlchemyError as e:
            logger.error(f"Team retrieval failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.put(
    "/{team_id}",
    response_model=schemas.TeamRead,
    summary="Update a team"
)
async def update_team(
    team_id: UUID,
    team_in: schemas.TeamUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Security(get_current_user, scopes=["write:teams"])
):
    """
    Update a team by its UUID.

    Args:
        team_id: UUID of the team.
        team_in: Team update data (e.g., name).
        db: Async database session.
        current_user: Authenticated user from Auth0.

    Returns:
        schemas.TeamRead: Updated team details.

    Raises:
        HTTPException: If the team is not found (404) or an error occurs (500).
    """
    with team_latency.labels(endpoint="/teams/{team_id}").time():
        team_requests.labels(endpoint="/teams/{team_id}", method="PUT").inc()
        try:
            team = await crud.get_team(db, str(team_id))
            if not team:
                raise HTTPException(status_code=404, detail="Team not found")
            updated_team = await crud.update_team(db, str(team_id), team_in)
            await log_audit_trail(db, str(team_id), "update", current_user["sub"], {"updates": team_in.dict(exclude_unset=True)})
            return updated_team
        except sa.exc.SQLAlchemyError as e:
            logger.error(f"Team update failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.delete(
    "/{team_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a team"
)
async def delete_team(
    team_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Security(get_current_user, scopes=["write:teams"])
):
    """
    Delete a team by its UUID.

    Args:
        team_id: UUID of the team.
        db: Async database session.
        current_user: Authenticated user from Auth0.

    Raises:
        HTTPException: If the team is not found (404) or an error occurs (500).
    """
    with team_latency.labels(endpoint="/teams/{team_id}").time():
        team_requests.labels(endpoint="/teams/{team_id}", method="DELETE").inc()
        try:
            success = await crud.delete_team(db, str(team_id))
            if not success:
                raise HTTPException(status_code=404, detail="Team not found")
            await log_audit_trail(db, str(team_id), "delete", current_user["sub"])
        except sa.exc.SQLAlchemyError as e:
            logger.error(f"Team deletion failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.post(
    "/{team_id}/insights",
    response_model=schemas.TeamInsightsResponse,
    summary="Get AI-driven team insights"
)
async def get_team_insights(
    team_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Security(get_current_user, scopes=["read:teams", "write:teams"])
):
    """
    Retrieve AI-driven insights for a team based on project and workflow metrics.

    Uses Grok 3 or Llama 3.1 to analyze team performance, project activity, and workflow
    run data, providing insights like team productivity or bottleneck detection.

    Args:
        team_id: UUID of the team.
        db: Async database session.
        current_user: Authenticated user from Auth0.

    Returns:
        schemas.TeamInsightsResponse: AI-generated team insights.

    Raises:
        HTTPException: If the team is not found (404) or AI processing fails (500).
    """
    with team_latency.labels(endpoint="/teams/{team_id}/insights").time():
        team_requests.labels(endpoint="/teams/{team_id}/insights", method="POST").inc()
        try:
            team = await crud.get_team(db, str(team_id))
            if not team:
                raise HTTPException(status_code=404, detail="Team not found")
            # Fetch project and workflow run data for the team
            projects = await db.execute(
                select(Project).filter_by(team_id=str(team_id))
            )
            project_ids = [p.id for p in projects.scalars().all()]
            runs = await db.execute(
                select(WorkflowRun)
                .filter(WorkflowRun.workflow_id.in_(
                    select(Workflow.id).filter_by(project_id.in_(project_ids))
                ))
                .limit(100)
            )
            run_data = [run.metadata for run in runs.scalars().all()]
            insights = await suggest_team_insights(team.name, project_ids, run_data)
            await log_audit_trail(db, str(team_id), "insights", current_user["sub"], {"insights": insights})
            return schemas.TeamInsightsResponse(insights=insights)
        except Exception as e:
            logger.error(f"Team insights failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
```
