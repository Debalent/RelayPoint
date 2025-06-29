# crud/team.py
from sqlalchemy.orm import Session
import app.models.team as models
import app.schemas.team as schemas

def create_team(db: Session, team_in: schemas.TeamCreate):
    db_obj = models.Team(**team_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_team(db: Session, id):
    return db.query(models.Team).filter(models.Team.id == id).first()

# plus get_teams, delete_team…
