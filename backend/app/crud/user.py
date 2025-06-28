# backend/app/crud/user.py

import uuid
import datetime
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from ..models.user import User
from ..schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int) -> User | None:
    """Fetch a user by their database ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_phone(db: Session, phone: str) -> User | None:
    """Fetch a user by their unique phone number."""
    return db.query(User).filter(User.phone == phone).first()


def authenticate_user(db: Session, phone: str, password: str) -> User | None:
    """
    Verify phone/password against stored hash.
    Returns the User on success, or None on failure.
    """
    user = get_user_by_phone(db, phone)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user


def create_user(db: Session, user_in: UserCreate) -> User:
    """Create a new user, hashing their password."""
    hashed = pwd_context.hash(user_in.password)
    db_user = User(
        phone=user_in.phone,
        full_name=user_in.full_name,
        is_manager=user_in.is_manager,
        hashed_password=hashed
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_password_reset_token(
    db: Session,
    user: User,
    expires_in: int = 3600
) -> str:
    """
    Generate a one-time reset token and expiry on the user record.
    Returns the raw token for delivery via SMS/email.
    """
    token = str(uuid.uuid4())
    user.reset_token = token
    user.reset_token_expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    db.add(user)
    db.commit()
    return token


def reset_user_password(
    db: Session,
    token: str,
    new_password: str
) -> User | None:
    """
    Validate a reset token, hash & store the new password, then clear token fields.
    Returns the updated User on success, or None if token invalid/expired.
    """
    user = db.query(User).filter(User.reset_token == token).first()
    if not user or not user.reset_token_expires or user.reset_token_expires < datetime.datetime.utcnow():
        return None

    # Hash & update password
    user.hashed_password = pwd_context.hash(new_password)
    user.reset_token = None
    user.reset_token_expires = None

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
