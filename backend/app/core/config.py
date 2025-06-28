# backend/app/core/config.py

import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # Project metadata
    PROJECT_NAME: str = "RelayPoint API"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    # Database connection
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:pass@localhost/relaypoint"
    )

    # Secrets & tokens
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change_me_in_prod")
    JWT_SECRET: str = os.getenv("JWT_SECRET", SECRET_KEY)
    ALGORITHM: str = "HS256"

    # Expiry settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7   # 1 week
    RESET_TOKEN_EXPIRE_SECONDS: int = 3600          # 1 hour

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
