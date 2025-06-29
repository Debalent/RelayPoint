from uuid import UUID
from pydantic import BaseModel

class TeamBase(BaseModel):
    name: str

class TeamCreate(TeamBase):
    owner_id: UUID

class TeamRead(TeamBase):
    id: UUID
    owner_id: UUID

    class Config:
        orm_mode = True
