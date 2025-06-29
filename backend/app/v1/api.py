# backend/app/api/v1/api.py

from fastapi import APIRouter
from .endpoints import auth, users

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
