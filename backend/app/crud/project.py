# backend/app/crud/project.py
from typing import List, Optional
from sqlalchemy.orm import Session
import app.models.project as models
import app.schemas.project as schemas

def create_project(db: Session, project_in: schemas.ProjectCreate) -> models.Project:
    db_obj = models.Project(**project_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_project(db: Session, project_id: str) -> Optional[models.Project]:
    return db.query(models.Project).filter(models.Project.id == project_id).first()

def get_projects(db: Session, skip: int = 0, limit: int = 100) -> List[models.Project]:
    return db.query(models.Project).offset(skip).limit(limit).all()

def get_projects_by_team(db: Session, team_id: str, skip: int = 0, limit: int = 100) -> List[models.Project]:
    return (
        db.query(models.Project)
          .filter(models.Project.team_id == team_id)
          .offset(skip)
          .limit(limit)
          .all()
    )

def delete_project(db: Session, project_id: str) -> bool:
    obj = get_project(db, project_id)
    if obj:
        db.delete(obj)
        db.commit()
        return True
    return False
