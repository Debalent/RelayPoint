from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.crud.team as crud
import app.schemas.team as schemas
from app.db.session import get_db

router = APIRouter(prefix="/teams", tags=["teams"])

@router.post(
    "/", 
    response_model=schemas.TeamRead, 
    status_code=status.HTTP_201_CREATED
)
def create_team(
    team_in: schemas.TeamCreate,
    db: Session = Depends(get_db),
):
    return crud.create_team(db, team_in)

@router.get(
    "/", 
    response_model=List[schemas.TeamRead]
)
def read_teams(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_teams(db, skip, limit)

@router.get(
    "/{team_id}",
    response_model=schemas.TeamRead
)
def read_team(
    team_id: UUID,
    db: Session = Depends(get_db),
):
    db_obj = crud.get_team(db, str(team_id))
    if not db_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )
    return db_obj

@router.delete(
    "/{team_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_team(
    team_id: UUID,
    db: Session = Depends(get_db),
):
    ok = crud.delete_team(db, str(team_id))
    if not ok:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Team not found",
        )
