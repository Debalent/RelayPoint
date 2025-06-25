from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ...schemas.user import UserCreate, UserRead
from ...crud.user import get_user_by_phone, create_user
from ...db import get_db

router = APIRouter()

@router.post("/users/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_phone(db, user_in.phone):
        raise HTTPException(status_code=400, detail="Phone already registered")
    return create_user(db, user_in)
