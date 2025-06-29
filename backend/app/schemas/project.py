# backend/app/schemas/project.py
from uuid import UUID
from pydantic import BaseModel

class ProjectBase(BaseModel):
    name: str

class ProjectCreate(ProjectBase):
    team_id: UUID

class ProjectRead(ProjectBase):
    id: UUID
    team_id: UUID

    class Config:
        orm_mode = True
