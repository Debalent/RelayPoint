# backend/app/api/v1/endpoints/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import Token, UserLogin
from app.crud.user import authenticate_user, create_access_token
from app.db import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticates user credentials and returns a JWT access token.
    Validates email/password against stored hash, then issues token with expiry.
    Scalable for multi-tenant auth, role-based access, and refresh token flows.
    """
    user = authenticate_user(db, user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
