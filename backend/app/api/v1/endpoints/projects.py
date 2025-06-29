# backend/app/api/v1/endpoints/projects.py
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import app.crud.project as crud
import app.schemas.project as schemas
from app.db.session import get_db

router = APIRouter(prefix="/projects", tags=["projects"])

@router.post("/", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(project_in: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db, project_in)

@router.get("/", response_model=List[schemas.ProjectRead])
def read_projects(
    skip: int = 0,
    limit: int = 100,
    team_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
):
    if team_id:
        return crud.get_projects_by_team(db, str(team_id), skip, limit)
    return crud.get_projects(db, skip, limit)

@router.get("/{project_id}", response_model=schemas.ProjectRead)
def read_project(project_id: UUID, db: Session = Depends(get_db)):
    db_obj = crud.get_project(db, str(project_id))
    if not db_obj:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_obj

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: UUID, db: Session = Depends(get_db)):
    ok = crud.delete_project(db, str(project_id))
    if not ok:
        raise HTTPException(status_code=404, detail="Project not found")
