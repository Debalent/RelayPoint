import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "RelayPoint API"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/relaypoint")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change_me_in_prod")

    class Config:
        env_file = ".env"

settings = Settings()
