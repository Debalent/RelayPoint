"""
Enterprise Configuration Module
Centralized configuration for all enterprise features
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
from functools import lru_cache
import os

class Settings(BaseSettings):
    """Enterprise settings with validation"""
    
    # Core
    PROJECT_NAME: str = "RelayPoint Enterprise"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    APP_VERSION: str = "2.0.0"
    
    # Database
    DATABASE_URL: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:19006",
        "https://app.relaypoint.ai"
    ]
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Enterprise Features
    ENABLE_RATE_LIMITING: bool = True
    ENABLE_CACHING: bool = True
    ENABLE_MULTI_TENANCY: bool = True
    
    # Monitoring
    PROMETHEUS_ENABLED: bool = True
    SENTRY_DSN: Optional[str] = None
    
    # Default tier for new signups
    DEFAULT_PLAN_TIER: str = "FREE"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Parse CORS_ORIGINS if it's a string
        if isinstance(self.CORS_ORIGINS, str):
            self.CORS_ORIGINS = [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        if isinstance(self.ALLOWED_HOSTS, str):
            self.ALLOWED_HOSTS = [host.strip() for host in self.ALLOWED_HOSTS.split(",")]

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

# Global settings instance
settings = get_settings()
