# backend/app/core/security.py

from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Generates a signed JWT access token for authenticated users.
    Embeds user identity and expiry metadata into the token payload.

    Strategic Role:
    - Enables stateless session management across distributed services.
    - Scalable for role-based access, token refresh flows, and mobile clients.
    - Securely encodes user claims using environment-based secret key.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
