# api/v1/endpoints/teams.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import app.crud.team as crud
import app.schemas.team as schemas
from app.db.session import get_db

router = APIRouter(prefix="/teams", tags=["teams"])

@router.post("/", response_model=schemas.TeamRead, status_code=201)
def create_team(team_in: schemas.TeamCreate, db: Session = Depends(get_db)):
    return crud.create_team(db, team_in)

# GET /teams, GET /teams/{id}, DELETE /teams/{id} …
