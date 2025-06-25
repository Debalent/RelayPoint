from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    phone: str = Field(..., example="+15551231234")
    full_name: str
    password: str

class UserRead(BaseModel):
    id: int
    phone: str
    full_name: str
    is_manager: bool

    class Config:
        orm_mode = True  # Allows reading from SQLAlchemy models directly
