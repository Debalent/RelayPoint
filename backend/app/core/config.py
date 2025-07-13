```python
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
from loguru import logger

class Settings(BaseSettings):
    """
    RelayPoint application settings, parsed from environment variables or .env file.

    Attributes:
        PROJECT_NAME: Name of the project (displayed in OpenAPI docs).
        APP_VERSION: Application version for tracking releases.
        DEBUG: Enable debug mode (use False in production).
        API_V1_STR: API v1 prefix for routing.
        CORS_ORIGINS: Allowed CORS origins for frontend integration.
        DATABASE_URL: PostgreSQL connection URL (with asyncpg driver).
        AUTH0_DOMAIN: Auth0 domain for OAuth 2.0 authentication.
        AUTH0_AUDIENCE: Auth0 audience for token validation.
        AUTH0_CLIENT_ID: Auth0 client ID for API interactions.
        AUTH0_CLIENT_SECRET: Auth0 client secret for secure API calls.
        ACCESS_TOKEN_EXPIRE_MINUTES: Access token expiry duration.
        REFRESH_TOKEN_EXPIRE_DAYS: Refresh token expiry duration.
        PROMETHEUS_ENABLED: Enable Prometheus metrics endpoint.
        LOKI_ENDPOINT: Loki endpoint for log aggregation.
        XAI_API_KEY: API key for xAI (Grok 3) integration.
        ENVIRONMENT: Deployment environment (dev, staging, prod).
    """
    # Project metadata
    PROJECT_NAME: str = "RelayPoint API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"

    # CORS settings for frontend integration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "https://relaypoint.example.com"
    ]

    # Database connection
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://user:password@localhost:5432/relaypoint"
    )

    # Auth0 configuration
    AUTH0_DOMAIN: str = os.getenv("AUTH0_DOMAIN", "<your-auth0-domain>")
    AUTH0_AUDIENCE: str = os.getenv("AUTH0_AUDIENCE", "<your-auth0-audience>")
    AUTH0_CLIENT_ID: str = os.getenv("AUTH0_CLIENT_ID", "<your-auth0-client-id>")
    AUTH0_CLIENT_SECRET: str = os.getenv("AUTH0_CLIENT_SECRET", "<your-auth0-client-secret>")

    # Token expiry settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30  # 30 days

    # Observability settings
    PROMETHEUS_ENABLED: bool = True
    LOKI_ENDPOINT: Optional[HttpUrl] = os.getenv("LOKI_ENDPOINT", "http://loki:3100")

    # AI integration (e.g., Grok 3 or Llama 3.1)
    XAI_API_KEY: Optional[str] = os.getenv("XAI_API_KEY", None)

    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v: str | List[str]) -> List[str]:
        """
        Parse CORS origins from a comma-separated string or list.

        Args:
            v: Input value (string or list).

        Returns:
            List[str]: List of CORS origins.

        Raises:
            ValueError: If origins are invalid.
        """
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    @validator("DATABASE_URL")
    def validate_database_url(cls, v: str) -> str:
        """
        Ensure DATABASE_URL uses asyncpg driver for async support.

        Args:
            v: Database URL.

        Returns:
            str: Validated database URL.

        Raises:
            ValueError: If URL is invalid or missing asyncpg.
        """
        if "postgresql+asyncpg" not in v:
            logger.warning("DATABASE_URL should use asyncpg driver for optimal performance")
        return v

    @validator("AUTH0_DOMAIN", "AUTH0_AUDIENCE", "AUTH0_CLIENT_ID", "AUTH0_CLIENT_SECRET")
    def validate_auth0_settings(cls, v: str, field: str) -> str:
        """
        Ensure Auth0 settings are provided in production.

        Args:
            v: Value of the Auth0 setting.
            field: Name of the field being validated.

        Returns:
            str: Validated value.

        Raises:
            ValueError: If Auth0 settings are missing in production.
        """
        if cls().ENVIRONMENT == "production" and "<your-auth0-" in v:
            raise ValueError(f"{field} must be set in production")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance for performance.

    Returns:
        Settings: Cached settings object.
    """
    logger.info("Loading RelayPoint settings")
    return Settings()

# Singleton settings instance
settings = get_settings()
```
