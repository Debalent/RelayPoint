"""
Enterprise Multi-Tenancy & White-Labeling System
Complete tenant isolation, custom branding, and SaaS features
"""

from sqlalchemy import Column, String, Integer, Boolean, JSON, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import Dict, Any, Optional, List
from datetime import datetime
import structlog
from enum import Enum
import uuid

logger = structlog.get_logger()

Base = declarative_base()


class TenantStatus(str, Enum):
    """Tenant account status"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TRIAL = "trial"
    CANCELLED = "cancelled"
    PENDING = "pending"


class PlanTier(str, Enum):
    """Subscription plan tiers"""
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"


class Tenant(Base):
    """
    Multi-tenant organization model
    Complete isolation with custom branding and configuration
    """
    __tablename__ = "tenants"
    
    # Core Identity
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)  # For custom domains
    domain = Column(String(255), unique=True, nullable=True)  # Custom domain (e.g., acme.relaypoint.ai)
    
    # Status & Subscription
    status = Column(String(20), default=TenantStatus.TRIAL.value)
    plan_tier = Column(String(20), default=PlanTier.FREE.value)
    subscription_id = Column(String(100), nullable=True)  # Stripe subscription ID
    trial_ends_at = Column(DateTime, nullable=True)
    subscription_starts_at = Column(DateTime, nullable=True)
    subscription_ends_at = Column(DateTime, nullable=True)
    
    # Limits & Quotas
    max_users = Column(Integer, default=5)
    max_workflows = Column(Integer, default=10)
    max_executions_per_month = Column(Integer, default=1000)
    max_storage_gb = Column(Integer, default=5)
    
    # Current Usage
    current_users = Column(Integer, default=0)
    current_workflows = Column(Integer, default=0)
    current_executions_this_month = Column(Integer, default=0)
    current_storage_gb = Column(Integer, default=0)
    
    # White-Labeling & Branding
    branding = Column(JSON, default={
        "primary_color": "#4CAF50",
        "secondary_color": "#2196F3",
        "logo_url": None,
        "favicon_url": None,
        "company_name": None,
        "support_email": None,
        "support_url": None
    })
    
    # Custom Features & Configuration
    features = Column(JSON, default={
        "api_access": True,
        "custom_integrations": False,
        "advanced_analytics": False,
        "sso": False,
        "audit_logs": True,
        "custom_roles": False,
        "white_labeling": False,
        "priority_support": False,
        "dedicated_resources": False
    })
    
    settings = Column(JSON, default={
        "timezone": "UTC",
        "date_format": "YYYY-MM-DD",
        "language": "en",
        "notifications_enabled": True,
        "two_factor_required": False,
        "session_timeout_minutes": 480,
        "password_policy": {
            "min_length": 8,
            "require_uppercase": True,
            "require_numbers": True,
            "require_symbols": False
        }
    })
    
    # Metadata
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(36), nullable=True)
    
    # Database Isolation
    database_name = Column(String(100), nullable=True)  # For schema-per-tenant isolation
    
    # Relationships
    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    workflows = relationship("Workflow", back_populates="tenant", cascade="all, delete-orphan")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert tenant to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug,
            "domain": self.domain,
            "status": self.status,
            "plan_tier": self.plan_tier,
            "branding": self.branding,
            "features": self.features,
            "settings": self.settings,
            "limits": {
                "max_users": self.max_users,
                "max_workflows": self.max_workflows,
                "max_executions_per_month": self.max_executions_per_month,
                "max_storage_gb": self.max_storage_gb
            },
            "usage": {
                "users": self.current_users,
                "workflows": self.current_workflows,
                "executions_this_month": self.current_executions_this_month,
                "storage_gb": self.current_storage_gb
            },
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class TenantManager:
    """Service for managing multi-tenant operations"""
    
    def __init__(self, db_session):
        self.db = db_session
    
    async def create_tenant(
        self,
        name: str,
        slug: str,
        plan_tier: PlanTier = PlanTier.FREE,
        admin_email: str = None,
        admin_name: str = None
    ) -> Tenant:
        """
        Create new tenant with complete setup
        - Create tenant record
        - Initialize database schema (if schema-per-tenant)
        - Create admin user
        - Setup default workflows
        """
        logger.info("Creating tenant", name=name, slug=slug, plan_tier=plan_tier)
        
        # Create tenant
        tenant = Tenant(
            name=name,
            slug=slug,
            plan_tier=plan_tier.value,
            status=TenantStatus.TRIAL.value if plan_tier == PlanTier.FREE else TenantStatus.ACTIVE.value
        )
        
        # Set plan-specific limits
        tenant = self._apply_plan_limits(tenant, plan_tier)
        
        # Set trial period for free tier
        if plan_tier == PlanTier.FREE:
            from datetime import timedelta
            tenant.trial_ends_at = datetime.utcnow() + timedelta(days=14)
        
        self.db.add(tenant)
        await self.db.commit()
        await self.db.refresh(tenant)
        
        # Create admin user if provided
        if admin_email and admin_name:
            await self._create_admin_user(tenant.id, admin_email, admin_name)
        
        # Initialize tenant resources
        await self._initialize_tenant_resources(tenant.id)
        
        logger.info("Tenant created successfully", tenant_id=tenant.id, name=name)
        return tenant
    
    def _apply_plan_limits(self, tenant: Tenant, plan_tier: PlanTier) -> Tenant:
        """Apply plan-specific limits and features"""
        limits_by_plan = {
            PlanTier.FREE: {
                "max_users": 5,
                "max_workflows": 10,
                "max_executions_per_month": 1000,
                "max_storage_gb": 5,
                "features": {
                    "api_access": True,
                    "custom_integrations": False,
                    "advanced_analytics": False,
                    "sso": False,
                    "audit_logs": True,
                    "custom_roles": False,
                    "white_labeling": False,
                    "priority_support": False,
                    "dedicated_resources": False
                }
            },
            PlanTier.STARTER: {
                "max_users": 25,
                "max_workflows": 50,
                "max_executions_per_month": 10000,
                "max_storage_gb": 25,
                "features": {
                    "api_access": True,
                    "custom_integrations": True,
                    "advanced_analytics": True,
                    "sso": False,
                    "audit_logs": True,
                    "custom_roles": True,
                    "white_labeling": False,
                    "priority_support": False,
                    "dedicated_resources": False
                }
            },
            PlanTier.PROFESSIONAL: {
                "max_users": 100,
                "max_workflows": 250,
                "max_executions_per_month": 100000,
                "max_storage_gb": 100,
                "features": {
                    "api_access": True,
                    "custom_integrations": True,
                    "advanced_analytics": True,
                    "sso": True,
                    "audit_logs": True,
                    "custom_roles": True,
                    "white_labeling": True,
                    "priority_support": True,
                    "dedicated_resources": False
                }
            },
            PlanTier.ENTERPRISE: {
                "max_users": -1,  # Unlimited
                "max_workflows": -1,
                "max_executions_per_month": -1,
                "max_storage_gb": -1,
                "features": {
                    "api_access": True,
                    "custom_integrations": True,
                    "advanced_analytics": True,
                    "sso": True,
                    "audit_logs": True,
                    "custom_roles": True,
                    "white_labeling": True,
                    "priority_support": True,
                    "dedicated_resources": True
                }
            }
        }
        
        plan_config = limits_by_plan.get(plan_tier, limits_by_plan[PlanTier.FREE])
        
        tenant.max_users = plan_config["max_users"]
        tenant.max_workflows = plan_config["max_workflows"]
        tenant.max_executions_per_month = plan_config["max_executions_per_month"]
        tenant.max_storage_gb = plan_config["max_storage_gb"]
        tenant.features = plan_config["features"]
        
        return tenant
    
    async def _create_admin_user(self, tenant_id: str, email: str, name: str):
        """Create admin user for tenant"""
        # Import here to avoid circular dependency
        from app.core.auth_enterprise import AuthService, UserRole
        
        # Create user with admin role
        # Implementation depends on your User model
        pass
    
    async def _initialize_tenant_resources(self, tenant_id: str):
        """Initialize default resources for new tenant"""
        # Create default workflows, templates, etc.
        pass
    
    async def upgrade_tenant(
        self,
        tenant_id: str,
        new_plan: PlanTier,
        subscription_id: Optional[str] = None
    ) -> Tenant:
        """Upgrade tenant to new plan tier"""
        tenant = await self.db.get(Tenant, tenant_id)
        
        if not tenant:
            raise ValueError(f"Tenant {tenant_id} not found")
        
        old_plan = tenant.plan_tier
        tenant.plan_tier = new_plan.value
        tenant.status = TenantStatus.ACTIVE.value
        tenant = self._apply_plan_limits(tenant, new_plan)
        
        if subscription_id:
            tenant.subscription_id = subscription_id
            tenant.subscription_starts_at = datetime.utcnow()
        
        await self.db.commit()
        
        logger.info(
            "Tenant upgraded",
            tenant_id=tenant_id,
            from_plan=old_plan,
            to_plan=new_plan.value
        )
        
        return tenant
    
    async def check_usage_limits(self, tenant_id: str, resource_type: str) -> bool:
        """Check if tenant is within usage limits"""
        tenant = await self.db.get(Tenant, tenant_id)
        
        if not tenant:
            return False
        
        # Unlimited for enterprise
        if tenant.plan_tier == PlanTier.ENTERPRISE.value:
            return True
        
        if resource_type == "users":
            return tenant.current_users < tenant.max_users
        elif resource_type == "workflows":
            return tenant.current_workflows < tenant.max_workflows
        elif resource_type == "executions":
            return tenant.current_executions_this_month < tenant.max_executions_per_month
        elif resource_type == "storage":
            return tenant.current_storage_gb < tenant.max_storage_gb
        
        return True
    
    async def update_branding(
        self,
        tenant_id: str,
        branding_config: Dict[str, Any]
    ) -> Tenant:
        """Update tenant branding configuration"""
        tenant = await self.db.get(Tenant, tenant_id)
        
        if not tenant:
            raise ValueError(f"Tenant {tenant_id} not found")
        
        # Check if white-labeling is enabled
        if not tenant.features.get("white_labeling", False):
            raise PermissionError("White-labeling not enabled for this plan")
        
        tenant.branding.update(branding_config)
        await self.db.commit()
        
        logger.info("Tenant branding updated", tenant_id=tenant_id)
        return tenant
    
    async def get_tenant_by_domain(self, domain: str) -> Optional[Tenant]:
        """Get tenant by custom domain"""
        from sqlalchemy import select
        
        result = await self.db.execute(
            select(Tenant).where(Tenant.domain == domain)
        )
        return result.scalar_one_or_none()
    
    async def suspend_tenant(self, tenant_id: str, reason: str = None):
        """Suspend tenant account"""
        tenant = await self.db.get(Tenant, tenant_id)
        
        if not tenant:
            raise ValueError(f"Tenant {tenant_id} not found")
        
        tenant.status = TenantStatus.SUSPENDED.value
        if reason:
            tenant.metadata["suspension_reason"] = reason
            tenant.metadata["suspended_at"] = datetime.utcnow().isoformat()
        
        await self.db.commit()
        logger.warning("Tenant suspended", tenant_id=tenant_id, reason=reason)
