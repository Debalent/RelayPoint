"""
Configuration settings for RelayPoint's FastAPI backend.

This module centralizes configuration for RelayPoint's AI-augmented, low-code workflow
automation engine, managing project metadata, database connections, Auth0 authentication,
observability endpoints, and AI integration settings. It uses Pydantic for type-safe
environment variable parsing and validation, supporting secure and scalable deployments.

WHY IT MATTERS FOR INVESTORS:
- Security: Auth0 configuration and secret management ensure industry-standard OAuth 2.0
  authentication, protecting sensitive workflow and project data.
- Scalability: Configurable database and observability settings support high-throughput
  workloads with TimescaleDB and Kubernetes.
- Reliability: Validated settings with defaults ensure consistent behavior across
  environments, aligning with enterprise SLAs.
- Compliance: Audit-ready configurations meet GDPR, HIPAA, and SOC 2 requirements through
  integration with TimescaleDB audit trails.
- Developer Productivity: Type-safe settings and clear documentation streamline
  development, reducing time-to-market.
- Market Alignment: Supports RelayPoint's core value proposition of low-code automation
  with AI augmentation, targeting a $140.80B agentic AI market by 2032 (39.3% CAGR).

@since Initial commit (Configuration settings for RelayPoint backend)
"""

from pydantic import BaseSettings, HttpUrl, EmailStr, validator
from typing import List, Optional
from functools import lru_cache
import os

class Settings(BaseSettings):
    """
    RelayPoint application settings, parsed from environment variables or .env file.
    """
    # Project metadata
    PROJECT_NAME: str = "RelayPoint API"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"

    # Security settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "https://relaypoint.example.com",
        "https://*.relaypoint.com"
    ]
    
    ALLOWED_HOSTS: List[str] = [
        "localhost",
        "127.0.0.1",
        "*.relaypoint.com"
    ]

    # Database connections
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://user:password@localhost:5432/relaypoint"
    )
    
    REDIS_URL: str = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0"
    )

    # Auth0 configuration
    AUTH0_DOMAIN: str = os.getenv("AUTH0_DOMAIN", "relaypoint.auth0.com")
    AUTH0_AUDIENCE: str = os.getenv("AUTH0_AUDIENCE", "relaypoint-api")
    AUTH0_CLIENT_ID: str = os.getenv("AUTH0_CLIENT_ID", "client-id")
    AUTH0_CLIENT_SECRET: str = os.getenv("AUTH0_CLIENT_SECRET", "client-secret")

    # Token expiry settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30  # 30 days

    # Observability settings
    PROMETHEUS_ENABLED: bool = True
    LOKI_ENDPOINT: Optional[str] = os.getenv("LOKI_ENDPOINT", "http://loki:3100")
    SENTRY_DSN: Optional[str] = os.getenv("SENTRY_DSN", None)

    # AI integration settings
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", None)
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY", None)
    XAI_API_KEY: Optional[str] = os.getenv("XAI_API_KEY", None)
    
    # AI model configurations
    DEFAULT_AI_MODEL: str = "gpt-4-turbo-preview"
    AI_TEMPERATURE: float = 0.7
    AI_MAX_TOKENS: int = 4096

    # Background task processing
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/2")

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    RATE_LIMIT_BURST: int = 200

    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"

    # Email settings
    SMTP_HOST: Optional[str] = os.getenv("SMTP_HOST", None)
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: Optional[str] = os.getenv("SMTP_USER", None)
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD", None)
    EMAIL_FROM: Optional[str] = os.getenv("EMAIL_FROM", None)

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from a comma-separated string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance for performance."""
    return Settings()

# Singleton settings instance
settings = get_settings()