```python
"""
FastAPI endpoints for managing projects in RelayPoint.

This module defines API endpoints for creating, reading, updating, and deleting projects,
which serve as logical containers for workflows in RelayPoint's AI-augmented, low-code
workflow automation engine. Projects link to teams, workflows, and audit trails, supporting
enterprise-grade features like resilience, observability, and AI-driven optimizations.

WHY IT MATTERS FOR INVESTORS:
- Scalability: Integrates with PostgreSQL and TimescaleDB for high-throughput storage of
  project and workflow data, supporting enterprise workloads.
- Reliability: Robust error handling, audit trails, and rollback support ensure consistent
  operations, aligning with enterprise SLAs.
- Compliance: Audit-ready project operations meet GDPR, HIPAA, and SOC 2 requirements,
  appealing to regulated industries like finance and healthcare.
- Developer Productivity: Type-safe endpoints and AI-driven suggestions (via Grok 3 or
  Llama 3.1) streamline development, reducing time-to-market.
- Market Alignment: Supports RelayPoint's core value proposition of low-code automation
  with AI augmentation, targeting a $140.80B agentic AI market by 2032 (39.3% CAGR).

@since Initial commit (Project endpoints for RelayPoint backend)
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from prometheus_client import Counter, Histogram
from loguru import logger
import app.crud.project as crud
import app.schemas.project as schemas
from app.db.session import get_async_db
from app.auth.auth0 import verify_auth0_token, get_current_user
from app.models import Project, WorkflowRun
from app.ai.workflow_coach import suggest_workflow_optimizations

# Prometheus metrics for observability
project_requests = Counter("relaypoint_project_requests_total", "Total project requests", ["endpoint", "method"])
project_latency = Histogram("relaypoint_project_request_latency_seconds", "Project request latency", ["endpoint"])
audit_trail_logs = Counter("relaypoint_project_audit_trails_total", "Total audit trail logs", ["operation"])

# OAuth2 configuration for Auth0
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="https://<your-auth0-domain>/oauth/token")

# FastAPI router for project endpoints
router = APIRouter(prefix="/projects", tags=["projects"])

async def log_audit_trail(
    db: AsyncSession,
    project_id: str,
    operation: str,
    user_id: str,
    metadata: Optional[dict] = None
) -> None:
    """
    Logs an audit trail for project operations to TimescaleDB.

    Args:
        db: Async database session.
        project_id: UUID of the project.
        operation: Operation performed (e.g., 'create', 'delete').
        user_id: ID of the user performing the operation.
        metadata: Optional additional metadata.

    Raises:
        sa.exc.SQLAlchemyError: If the audit trail fails to save.
    """
    try:
        audit_trail = WorkflowRun(
            workflow_id=None,  # Project-level audit, not tied to a specific workflow
            timestamp=func.now(),
            status=operation,
            metadata={"project_id": project_id, "user_id": user_id, **(metadata or {})}
        )
        db.add(audit_trail)
        await db.commit()
        audit_trail_logs.labels(operation=operation).inc()
        logger.info(f"Audit trail logged for project {project_id}: {operation}")
    except sa.exc.SQLAlchemyError as e:
        logger.error(f"Failed to log audit trail: {str(e)}")
        raise

@router.post(
    "/",
    response_model=schemas.ProjectRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project"
)
async def create_project(
    project_in: schemas.ProjectCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Security(get_current_user, scopes=["write:projects"])
):
    """
    Create a new project with audit trail logging.

    Args:
        project_in: Project creation data (name, team_id, etc.).
        db: Async database session.
        current_user: Authenticated user from Auth0.

    Returns:
        schemas.ProjectRead: Created project details.

    Raises:
        HTTPException: If the team_id is invalid or the project creation fails.
    """
    with project_latency.labels(endpoint="/projects").time():
        project_requests.labels(endpoint="/projects", method="POST").inc()
        try:
            # Validate team_id if provided
            if project_in.team_id:
                team = await db.execute(select(Team).filter_by(id=str(project_in.team_id)))
                if not team.scalars().first():
                    raise HTTPException(status_code=400, detail="Invalid team_id")

            project = await crud.create_project(db, project_in)
            await log_audit_trail(db, str(project.id), "create", current_user["sub"], {"project_name": project.name})
            return project
        except sa.exc.SQLAlchemyError as e:
            logger.error(f"Project creation failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/",
    response_model=List[schemas.ProjectRead],
    summary="List projects"
)
async def read_projects(
    skip: int = 0,
    limit: int = 100,
    team_id: Optional[UUID] = None,
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Security(get_current_user, scopes=["read:projects"])
):
    """
    Retrieve a list of projects, optionally filtered by team_id.

    Args:
        skip: Number of projects to skip (pagination).
        limit: Maximum number of projects to return.
        team_id: Optional UUID to filter projects by team.
        db: Async database session.
        current_user: Authenticated user from Auth0.

    Returns:
        List[schemas.ProjectRead]: List of project details.

    Raises:
        HTTPException: If the team_id is invalid.
    """
    with project_latency.labels(endpoint="/projects").time():
        project_requests.labels(endpoint="/projects", method="GET").inc()
        try:
            if team_id:
                team = await db.execute(select(Team).filter_by(id=str(team_id)))
                if not team.scalars().first():
                    raise HTTPException(status_code=400, detail="Invalid team_id")
                projects = await crud.get_projects_by_team(db, str(team_id), skip, limit)
            else:
                projects = await crud.get_projects(db, skip, limit)
            await log_audit_trail(db, "all", "list", current_user["sub"], {"skip": skip, "limit": limit})
            return projects
        except sa.exc.SQLAlchemyError as e:
            logger.error(f"Project listing failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.get(
    "/{project_id}",
    response_model=schemas.ProjectRead,
    summary="Get a project by ID"
)
async def read_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Security(get_current_user, scopes=["read:projects"])
):
    """
    Retrieve a project by its UUID.

    Args:
        project_id: UUID of the project.
        db: Async database session.
        current_user: Authenticated user from Auth0.

    Returns:
        schemas.ProjectRead: Project details.

    Raises:
        HTTPException: If the project is not found (404) or an error occurs (500).
    """
    with project_latency.labels(endpoint="/projects/{project_id}").time():
        project_requests.labels(endpoint="/projects/{project_id}", method="GET").inc()
        try:
            project = await crud.get_project(db, str(project_id))
            if not project:
                raise HTTPException(status_code=404, detail="Project not found")
            await log_audit_trail(db, str(project_id), "read", current_user["sub"])
            return project
        except sa.exc.SQLAlchemyError as e:
            logger.error(f"Project retrieval failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.put(
    "/{project_id}",
    response_model=schemas.ProjectRead,
    summary="Update a project"
)
async def update_project(
    project_id: UUID,
    project_in: schemas.ProjectUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Security(get_current_user, scopes=["write:projects"])
):
    """
    Update a project by its UUID.

    Args:
        project_id: UUID of the project.
        project_in: Project update data (e.g., name, team_id).
        db: Async database session.
        current_user: Authenticated user from Auth0.

    Returns:
        schemas.ProjectRead: Updated project details.

    Raises:
        HTTPException: If the project or team_id is invalid.
    """
    with project_latency.labels(endpoint="/projects/{project_id}").time():
        project_requests.labels(endpoint="/projects/{project_id}", method="PUT").inc()
        try:
            project = await crud.get_project(db, str(project_id))
            if not project:
                raise HTTPException(status_code=404, detail="Project not found")
            if project_in.team_id:
                team = await db.execute(select(Team).filter_by(id=str(project_in.team_id)))
                if not team.scalars().first():
                    raise HTTPException(status_code=400, detail="Invalid team_id")
            updated_project = await crud.update_project(db, str(project_id), project_in)
            await log_audit_trail(db, str(project_id), "update", current_user["sub"], {"updates": project_in.dict(exclude_unset=True)})
            return updated_project
        except sa.exc.SQLAlchemyError as e:
            logger.error(f"Project update failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a project"
)
async def delete_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Security(get_current_user, scopes=["write:projects"])
):
    """
    Delete a project by its UUID.

    Args:
        project_id: UUID of the project.
        db: Async database session.
        current_user: Authenticated user from Auth0.

    Raises:
        HTTPException: If the project is not found (404) or an error occurs (500).
    """
    with project_latency.labels(endpoint="/projects/{project_id}").time():
        project_requests.labels(endpoint="/projects/{project_id}", method="DELETE").inc()
        try:
            success = await crud.delete_project(db, str(project_id))
            if not success:
                raise HTTPException(status_code=404, detail="Project not found")
            await log_audit_trail(db, str(project_id), "delete", current_user["sub"])
        except sa.exc.SQLAlchemyError as e:
            logger.error(f"Project deletion failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

@router.post(
    "/{project_id}/optimize",
    response_model=schemas.WorkflowOptimizationResponse,
    summary="Get AI-driven workflow optimizations for a project"
)
async def optimize_project_workflows(
    project_id: UUID,
    db: AsyncSession = Depends(get_async_db),
    current_user: dict = Security(get_current_user, scopes=["read:projects", "write:projects"])
):
    """
    Retrieve AI-driven workflow optimization suggestions for a project.

    Uses Grok 3 or Llama 3.1 to suggest optimizations (e.g., parallelizing steps,
    adding retries) based on project workflows and audit trails.

    Args:
        project_id: UUID of the project.
        db: Async database session.
        current_user: Authenticated user from Auth0.

    Returns:
        schemas.WorkflowOptimizationResponse: AI-generated optimization suggestions.

    Raises:
        HTTPException: If the project is not found or AI processing fails.
    """
    with project_latency.labels(endpoint="/projects/{project_id}/optimize").time():
        project_requests.labels(endpoint="/projects/{project_id}/optimize", method="POST").inc()
        try:
            project = await crud.get_project(db, str(project_id))
            if not project:
                raise HTTPException(status_code=404, detail="Project not found")
            # Fetch recent workflow runs for analysis
            runs = await db.execute(
                select(WorkflowRun)
                .filter_by(workflow_id__in=(
                    select(Workflow.id).filter_by(project_id=str(project_id))
                ))
                .limit(100)
            )
            run_data = [run.metadata for run in runs.scalars().all()]
            suggestions = await suggest_workflow_optimizations(project.config, run_data)
            await log_audit_trail(db, str(project_id), "optimize", current_user["sub"], {"suggestions": suggestions})
            return schemas.WorkflowOptimizationResponse(suggestions=suggestions)
        except Exception as e:
            logger.error(f"Workflow optimization failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
```
