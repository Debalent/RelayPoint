# app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, core
from app.db import get_db
from passlib.context import CryptContext
from jose import jwt, JWTError

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register", response_model=schemas.User)
def register(data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_phone(db, data.phone)
    if user:
        raise HTTPException(status_code=400, detail="Phone already registered")
    hashed = pwd_ctx.hash(data.password)
    return crud.create_user(db, data, hashed)

@router.post("/login", response_model=schemas.Token)
def login(data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = crud.get_user_by_phone(db, data.phone)
    if not user or not pwd_ctx.verify(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    payload = {"sub": str(user.id)}
    token = jwt.encode(payload, core.JWT_SECRET, algorithm=core.ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}
