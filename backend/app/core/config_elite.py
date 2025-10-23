"""
Elite Configuration for RelayPoint - Enterprise-Grade Workflow Automation Platform

This module provides comprehensive configuration management for RelayPoint's advanced
AI-powered workflow automation platform, supporting enterprise features, scalability,
and security requirements.
"""

import os
import secrets
from typing import Any, Dict, Optional, List, Union
from pydantic import BaseSettings, validator, Field
from pydantic_settings import BaseSettings as PydanticBaseSettings


class Settings(PydanticBaseSettings):
    """Elite configuration settings for RelayPoint."""
    
    # Core API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "RelayPoint Elite"
    PROJECT_VERSION: str = "2.0.0"
    PROJECT_DESCRIPTION: str = "Enterprise AI-Powered Workflow Automation Platform"
    
    # Security Configuration
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    PASSWORD_MIN_LENGTH: int = 8
    REQUIRE_2FA: bool = False
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="postgresql://relaypoint:secure_password@localhost:5432/relaypoint_elite",
        description="PostgreSQL database connection string"
    )
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30
    DATABASE_POOL_TIMEOUT: int = 30
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600  # 1 hour
    REDIS_SESSION_TTL: int = 86400  # 24 hours
    
    # Celery Task Queue Configuration
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    CELERY_ACCEPT_CONTENT: List[str] = ["json"]
    CELERY_TIMEZONE: str = "UTC"
    
    # AI Provider Configuration
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_AI_API_KEY: str = ""
    COHERE_API_KEY: str = ""
    HUGGINGFACE_API_KEY: str = ""
    
    # AI Model Configuration
    DEFAULT_AI_MODEL: str = "gpt-4-turbo-preview"
    FALLBACK_AI_MODEL: str = "gpt-3.5-turbo"
    MAX_TOKENS: int = 4096
    TEMPERATURE: float = 0.7
    AI_REQUEST_TIMEOUT: int = 60
    MAX_AI_REQUESTS_PER_MINUTE: int = 60
    
    # WebSocket Configuration
    WEBSOCKET_MAX_CONNECTIONS: int = 1000
    WEBSOCKET_HEARTBEAT_INTERVAL: int = 30
    WEBSOCKET_MESSAGE_QUEUE_SIZE: int = 100
    
    # File Upload Configuration
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: List[str] = [
        ".txt", ".pdf", ".doc", ".docx", ".json", ".csv", 
        ".xlsx", ".pptx", ".md", ".py", ".js", ".ts"
    ]
    UPLOAD_PATH: str = "/tmp/uploads"
    
    # Rate Limiting Configuration
    RATE_LIMIT_REQUESTS: int = 1000
    RATE_LIMIT_WINDOW: int = 3600  # 1 hour
    RATE_LIMIT_BURST: int = 100
    
    # Monitoring & Observability
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    SENTRY_DSN: str = ""
    JAEGER_ENDPOINT: str = ""
    LOG_LEVEL: str = "INFO"
    STRUCTURED_LOGGING: bool = True
    
    # Enterprise Features
    ENABLE_AUDIT_LOGGING: bool = True
    ENABLE_COLLABORATION: bool = True
    ENABLE_ADVANCED_ANALYTICS: bool = True
    ENABLE_WHITE_LABELING: bool = True
    ENABLE_SSO: bool = True
    ENABLE_RBAC: bool = True
    
    # Email Configuration
    SMTP_TLS: bool = True
    SMTP_PORT: int = 587
    SMTP_HOST: str = ""
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAILS_FROM_EMAIL: str = "noreply@relaypoint.ai"
    EMAILS_FROM_NAME: str = "RelayPoint Elite"
    EMAIL_TEMPLATES_DIR: str = "email-templates"
    
    # Environment Configuration
    ENVIRONMENT: str = Field(default="development", regex="^(development|staging|production)$")
    DEBUG: bool = False
    TESTING: bool = False
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000", 
        "https://app.relaypoint.ai",
        "https://relaypoint.ai"
    ]
    
    # Subscription Tier Limits
    TIER_LIMITS: Dict[str, Dict[str, Any]] = {
        "free": {
            "workflows_per_month": 10,
            "ai_requests_per_month": 100,
            "team_members": 1,
            "storage_gb": 1,
            "custom_integrations": 0,
            "api_requests_per_day": 1000,
            "advanced_analytics": False,
            "priority_support": False
        },
        "pro": {
            "workflows_per_month": 100,
            "ai_requests_per_month": 2000,
            "team_members": 10,
            "storage_gb": 25,
            "custom_integrations": 5,
            "api_requests_per_day": 10000,
            "advanced_analytics": True,
            "priority_support": False
        },
        "enterprise": {
            "workflows_per_month": -1,  # unlimited
            "ai_requests_per_month": -1,
            "team_members": -1,
            "storage_gb": 500,
            "custom_integrations": -1,
            "api_requests_per_day": -1,
            "advanced_analytics": True,
            "priority_support": True,
            "sso": True,
            "audit_logs": True,
            "custom_branding": True
        }
    }
    
    # Analytics & Reporting
    ANALYTICS_RETENTION_DAYS: int = 365
    ENABLE_REAL_TIME_ANALYTICS: bool = True
    ANALYTICS_BATCH_SIZE: int = 1000
    
    # Security Headers
    SECURITY_HEADERS: Dict[str, str] = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'"
    }
    
    # Workflow Execution
    MAX_WORKFLOW_STEPS: int = 50
    WORKFLOW_TIMEOUT_SECONDS: int = 3600  # 1 hour
    MAX_CONCURRENT_WORKFLOWS: int = 100
    WORKFLOW_RETRY_ATTEMPTS: int = 3
    
    # Cache Configuration
    CACHE_DEFAULT_TTL: int = 300  # 5 minutes
    CACHE_USER_TTL: int = 900  # 15 minutes
    CACHE_WORKFLOW_TTL: int = 1800  # 30 minutes
    
    # Search Configuration
    ELASTICSEARCH_URL: str = ""
    ENABLE_FULL_TEXT_SEARCH: bool = False
    SEARCH_INDEX_PREFIX: str = "relaypoint"
    
    # Backup Configuration
    BACKUP_ENABLED: bool = True
    BACKUP_SCHEDULE: str = "0 2 * * *"  # Daily at 2 AM
    BACKUP_RETENTION_DAYS: int = 30
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    @validator("DEBUG", pre=True)
    def parse_debug(cls, v: Union[str, bool]) -> bool:
        if isinstance(v, str):
            return v.lower() in ("true", "1", "yes", "on")
        return v
    
    @validator("ENVIRONMENT")
    def validate_environment(cls, v: str) -> str:
        if v not in ["development", "staging", "production"]:
            raise ValueError("Environment must be development, staging, or production")
        return v
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"
    
    @property
    def database_url_async(self) -> str:
        """Get async database URL for SQLAlchemy."""
        return self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        env_prefix = "RELAYPOINT_"


# Global settings instance
settings = Settings()


# Environment-specific configurations
def get_database_config() -> Dict[str, Any]:
    """Get database configuration based on environment."""
    base_config = {
        "pool_size": settings.DATABASE_POOL_SIZE,
        "max_overflow": settings.DATABASE_MAX_OVERFLOW,
        "pool_timeout": settings.DATABASE_POOL_TIMEOUT,
        "pool_pre_ping": True,
    }
    
    if settings.is_production:
        base_config.update({
            "pool_size": 50,
            "max_overflow": 100,
            "pool_recycle": 3600,
        })
    
    return base_config


def get_logging_config() -> Dict[str, Any]:
    """Get logging configuration based on environment."""
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            },
            "structured": {
                "format": "%(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "structured" if settings.STRUCTURED_LOGGING else "default",
                "level": settings.LOG_LEVEL,
            },
        },
        "root": {
            "level": settings.LOG_LEVEL,
            "handlers": ["console"],
        },
    }