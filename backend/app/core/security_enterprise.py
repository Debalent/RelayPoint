"""
Enterprise Security & Audit Module for RelayPoint Elite

This module provides comprehensive security features including:
- Role-based access control (RBAC)
- Advanced audit logging
- Security monitoring and alerts
- Compliance reporting (SOC 2, GDPR, HIPAA)
- Multi-factor authentication
- API security and rate limiting
"""

import logging
import json
import hashlib
from typing import Dict, List, Optional, Any, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import uuid
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


class SecurityLevel(str, Enum):
    """Security clearance levels."""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    SECRET = "secret"
    TOP_SECRET = "top_secret"


class AuditEventType(str, Enum):
    """Types of audit events."""
    LOGIN = "login"
    LOGOUT = "logout"
    WORKFLOW_CREATE = "workflow_create"
    WORKFLOW_EXECUTE = "workflow_execute"
    WORKFLOW_DELETE = "workflow_delete"
    DATA_ACCESS = "data_access"
    DATA_EXPORT = "data_export"
    PERMISSION_CHANGE = "permission_change"
    SECURITY_VIOLATION = "security_violation"
    API_ACCESS = "api_access"
    SYSTEM_CONFIG = "system_config"


class PermissionType(str, Enum):
    """Permission types for RBAC."""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    DELETE = "delete"
    ADMIN = "admin"
    EXPORT = "export"
    SHARE = "share"


@dataclass
class Role:
    """Security role definition."""
    id: str
    name: str
    description: str
    permissions: Set[str]
    security_level: SecurityLevel
    created_at: datetime
    created_by: str
    is_system_role: bool = False


@dataclass
class User:
    """Enhanced user model with security features."""
    id: str
    email: str
    name: str
    roles: Set[str]
    security_clearance: SecurityLevel
    mfa_enabled: bool
    last_login: Optional[datetime]
    failed_login_attempts: int
    account_locked: bool
    session_timeout: int  # minutes
    password_last_changed: datetime
    created_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditEvent:
    """Audit event record."""
    id: str
    event_type: AuditEventType
    user_id: str
    resource_id: Optional[str]
    resource_type: Optional[str]
    action: str
    details: Dict[str, Any]
    ip_address: str
    user_agent: str
    timestamp: datetime
    session_id: Optional[str]
    risk_score: int  # 0-100
    compliance_tags: List[str]


@dataclass
class SecurityPolicy:
    """Security policy configuration."""
    id: str
    name: str
    description: str
    rules: Dict[str, Any]
    enforcement_level: str  # "advisory", "warning", "blocking"
    applicable_roles: Set[str]
    created_at: datetime
    updated_at: datetime


class EnterpriseSecurityManager:
    """
    Enterprise-grade security manager providing comprehensive
    access control, audit logging, and compliance features.
    """
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.roles: Dict[str, Role] = {}
        self.users: Dict[str, User] = {}
        self.audit_events: List[AuditEvent] = []
        self.security_policies: Dict[str, SecurityPolicy] = {}
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        
        # Security settings
        self.max_failed_logins = config.get("max_failed_logins", 5)
        self.session_timeout = config.get("session_timeout", 480)  # 8 hours
        self.password_min_length = config.get("password_min_length", 12)
        self.mfa_required_roles = config.get("mfa_required_roles", ["admin", "security"])
        
        # Initialize default roles
        self._initialize_default_roles()
        
        # Initialize security policies
        self._initialize_security_policies()
    
    def _initialize_default_roles(self):
        """Initialize default system roles."""
        default_roles = [
            Role(
                id="viewer",
                name="Viewer",
                description="Read-only access to workflows and data",
                permissions={"workflows:read", "data:read", "analytics:read"},
                security_level=SecurityLevel.INTERNAL,
                created_at=datetime.utcnow(),
                created_by="system",
                is_system_role=True
            ),
            Role(
                id="editor",
                name="Editor",
                description="Create and edit workflows",
                permissions={
                    "workflows:read", "workflows:write", "workflows:execute",
                    "data:read", "data:write", "analytics:read"
                },
                security_level=SecurityLevel.INTERNAL,
                created_at=datetime.utcnow(),
                created_by="system",
                is_system_role=True
            ),
            Role(
                id="admin",
                name="Administrator",
                description="Full system administration access",
                permissions={
                    "workflows:read", "workflows:write", "workflows:execute", "workflows:delete",
                    "data:read", "data:write", "data:export", "data:delete",
                    "analytics:read", "analytics:export",
                    "users:read", "users:write", "users:delete",
                    "roles:read", "roles:write", "roles:delete",
                    "system:config", "audit:read", "audit:export"
                },
                security_level=SecurityLevel.CONFIDENTIAL,
                created_at=datetime.utcnow(),
                created_by="system",
                is_system_role=True
            ),
            Role(
                id="security",
                name="Security Officer",
                description="Security and compliance management",
                permissions={
                    "audit:read", "audit:export", "security:read", "security:write",
                    "compliance:read", "compliance:export", "users:read", "roles:read"
                },
                security_level=SecurityLevel.SECRET,
                created_at=datetime.utcnow(),
                created_by="system",
                is_system_role=True
            )
        ]
        
        for role in default_roles:
            self.roles[role.id] = role
    
    def _initialize_security_policies(self):
        """Initialize default security policies."""
        policies = [
            SecurityPolicy(
                id="password_policy",
                name="Password Security Policy",
                description="Enforce strong password requirements",
                rules={
                    "min_length": 12,
                    "require_uppercase": True,
                    "require_lowercase": True,
                    "require_numbers": True,
                    "require_symbols": True,
                    "max_age_days": 90,
                    "history_count": 12
                },
                enforcement_level="blocking",
                applicable_roles={"*"},
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            SecurityPolicy(
                id="session_policy",
                name="Session Management Policy",
                description="Control user session behavior",
                rules={
                    "max_concurrent_sessions": 3,
                    "idle_timeout_minutes": 30,
                    "absolute_timeout_minutes": 480,
                    "require_reauth_for_sensitive": True
                },
                enforcement_level="blocking",
                applicable_roles={"*"},
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            SecurityPolicy(
                id="data_classification",
                name="Data Classification Policy",
                description="Classify and protect sensitive data",
                rules={
                    "auto_classify": True,
                    "encryption_required": ["confidential", "secret", "top_secret"],
                    "access_logging_required": ["confidential", "secret", "top_secret"],
                    "export_restrictions": {
                        "secret": ["security", "admin"],
                        "top_secret": ["security"]
                    }
                },
                enforcement_level="blocking",
                applicable_roles={"*"},
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        
        for policy in policies:
            self.security_policies[policy.id] = policy
    
    async def authenticate_user(self, 
                              email: str, 
                              password: str,
                              mfa_token: Optional[str] = None,
                              ip_address: str = "",
                              user_agent: str = "") -> Dict[str, Any]:
        """
        Authenticate user with enhanced security checks.
        
        Args:
            email: User email
            password: User password
            mfa_token: Multi-factor authentication token
            ip_address: Client IP address
            user_agent: Client user agent
            
        Returns:
            Authentication result with session info
        """
        try:
            # Find user by email
            user = None
            for u in self.users.values():
                if u.email.lower() == email.lower():
                    user = u
                    break
            
            if not user:
                await self._log_audit_event(
                    AuditEventType.LOGIN,
                    "unknown",
                    None,
                    None,
                    "failed_login_invalid_user",
                    {"email": email, "reason": "user_not_found"},
                    ip_address,
                    user_agent
                )
                return {"success": False, "error": "Invalid credentials"}
            
            # Check if account is locked
            if user.account_locked:
                await self._log_audit_event(
                    AuditEventType.LOGIN,
                    user.id,
                    None,
                    None,
                    "failed_login_account_locked",
                    {"email": email},
                    ip_address,
                    user_agent
                )
                return {"success": False, "error": "Account locked"}
            
            # Verify password (in real implementation, use proper hashing)
            if not self._verify_password(password, user):
                user.failed_login_attempts += 1
                
                if user.failed_login_attempts >= self.max_failed_logins:
                    user.account_locked = True
                    await self._log_audit_event(
                        AuditEventType.SECURITY_VIOLATION,
                        user.id,
                        None,
                        None,
                        "account_locked_too_many_failures",
                        {"email": email, "attempts": user.failed_login_attempts},
                        ip_address,
                        user_agent
                    )
                
                await self._log_audit_event(
                    AuditEventType.LOGIN,
                    user.id,
                    None,
                    None,
                    "failed_login_invalid_password",
                    {"email": email, "attempts": user.failed_login_attempts},
                    ip_address,
                    user_agent
                )
                return {"success": False, "error": "Invalid credentials"}
            
            # Check MFA if required
            if user.mfa_enabled or any(role in self.mfa_required_roles for role in user.roles):
                if not mfa_token or not self._verify_mfa_token(user, mfa_token):
                    await self._log_audit_event(
                        AuditEventType.LOGIN,
                        user.id,
                        None,
                        None,
                        "failed_login_invalid_mfa",
                        {"email": email},
                        ip_address,
                        user_agent
                    )
                    return {"success": False, "error": "Invalid MFA token", "requires_mfa": True}
            
            # Reset failed attempts on successful login
            user.failed_login_attempts = 0
            user.last_login = datetime.utcnow()
            
            # Create session
            session_id = str(uuid.uuid4())
            session_data = {
                "user_id": user.id,
                "created_at": datetime.utcnow(),
                "last_activity": datetime.utcnow(),
                "ip_address": ip_address,
                "user_agent": user_agent,
                "permissions": self._get_user_permissions(user)
            }
            
            self.active_sessions[session_id] = session_data
            
            # Log successful login
            await self._log_audit_event(
                AuditEventType.LOGIN,
                user.id,
                None,
                None,
                "successful_login",
                {"email": email},
                ip_address,
                user_agent,
                session_id=session_id
            )
            
            return {
                "success": True,
                "session_id": session_id,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "roles": list(user.roles),
                    "permissions": list(session_data["permissions"])
                }
            }
            
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return {"success": False, "error": "Authentication failed"}
    
    async def check_permission(self, 
                             session_id: str, 
                             permission: str,
                             resource_id: Optional[str] = None) -> bool:
        """
        Check if user has specific permission.
        
        Args:
            session_id: User session ID
            permission: Permission to check
            resource_id: Optional resource ID for resource-specific permissions
            
        Returns:
            True if user has permission
        """
        session = self.active_sessions.get(session_id)
        if not session:
            return False
        
        # Check session validity
        if not self._is_session_valid(session):
            return False
        
        # Update last activity
        session["last_activity"] = datetime.utcnow()
        
        # Check permission
        user_permissions = session.get("permissions", set())
        
        # Admin users have all permissions
        if "system:admin" in user_permissions:
            return True
        
        # Check direct permission
        if permission in user_permissions:
            return True
        
        # Check wildcard permissions
        permission_parts = permission.split(":")
        for i in range(len(permission_parts)):
            wildcard_perm = ":".join(permission_parts[:i+1]) + ":*"
            if wildcard_perm in user_permissions:
                return True
        
        return False
    
    async def log_data_access(self, 
                            session_id: str,
                            resource_type: str,
                            resource_id: str,
                            action: str,
                            data_classification: SecurityLevel = SecurityLevel.INTERNAL):
        """Log data access for audit trail."""
        session = self.active_sessions.get(session_id)
        if not session:
            return
        
        risk_score = self._calculate_risk_score(action, data_classification, session)
        
        await self._log_audit_event(
            AuditEventType.DATA_ACCESS,
            session["user_id"],
            resource_id,
            resource_type,
            action,
            {
                "data_classification": data_classification.value,
                "risk_score": risk_score
            },
            session["ip_address"],
            session["user_agent"],
            session_id=session_id,
            risk_score=risk_score
        )
    
    async def generate_compliance_report(self, 
                                       compliance_standard: str,
                                       start_date: datetime,
                                       end_date: datetime) -> Dict[str, Any]:
        """
        Generate compliance report for audit purposes.
        
        Args:
            compliance_standard: Standard to report on (SOC2, GDPR, HIPAA, etc.)
            start_date: Report start date
            end_date: Report end date
            
        Returns:
            Compliance report data
        """
        relevant_events = [
            event for event in self.audit_events
            if start_date <= event.timestamp <= end_date
            and compliance_standard.lower() in [tag.lower() for tag in event.compliance_tags]
        ]
        
        report = {
            "compliance_standard": compliance_standard,
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            "summary": {
                "total_events": len(relevant_events),
                "security_violations": len([e for e in relevant_events if e.event_type == AuditEventType.SECURITY_VIOLATION]),
                "data_access_events": len([e for e in relevant_events if e.event_type == AuditEventType.DATA_ACCESS]),
                "high_risk_events": len([e for e in relevant_events if e.risk_score >= 70])
            },
            "events": [
                {
                    "id": event.id,
                    "timestamp": event.timestamp.isoformat(),
                    "event_type": event.event_type.value,
                    "user_id": event.user_id,
                    "action": event.action,
                    "risk_score": event.risk_score,
                    "details": event.details
                }
                for event in relevant_events
            ]
        }
        
        # Add compliance-specific sections
        if compliance_standard.upper() == "GDPR":
            report["gdpr_specific"] = self._generate_gdpr_section(relevant_events)
        elif compliance_standard.upper() == "SOC2":
            report["soc2_specific"] = self._generate_soc2_section(relevant_events)
        elif compliance_standard.upper() == "HIPAA":
            report["hipaa_specific"] = self._generate_hipaa_section(relevant_events)
        
        return report
    
    def _verify_password(self, password: str, user: User) -> bool:
        """Verify user password (simplified for demo)."""
        # In real implementation, use proper password hashing (bcrypt, Argon2, etc.)
        return True  # Simplified for demo
    
    def _verify_mfa_token(self, user: User, token: str) -> bool:
        """Verify MFA token (simplified for demo)."""
        # In real implementation, integrate with TOTP/SMS/authenticator app
        return True  # Simplified for demo
    
    def _get_user_permissions(self, user: User) -> Set[str]:
        """Get all permissions for a user based on their roles."""
        permissions = set()
        for role_id in user.roles:
            role = self.roles.get(role_id)
            if role:
                permissions.update(role.permissions)
        return permissions
    
    def _is_session_valid(self, session: Dict[str, Any]) -> bool:
        """Check if session is still valid."""
        now = datetime.utcnow()
        
        # Check idle timeout
        idle_timeout = timedelta(minutes=30)
        if now - session["last_activity"] > idle_timeout:
            return False
        
        # Check absolute timeout
        absolute_timeout = timedelta(minutes=self.session_timeout)
        if now - session["created_at"] > absolute_timeout:
            return False
        
        return True
    
    def _calculate_risk_score(self, 
                            action: str, 
                            data_classification: SecurityLevel,
                            session: Dict[str, Any]) -> int:
        """Calculate risk score for an action."""
        base_score = 10
        
        # Increase score based on data classification
        classification_scores = {
            SecurityLevel.PUBLIC: 0,
            SecurityLevel.INTERNAL: 10,
            SecurityLevel.CONFIDENTIAL: 30,
            SecurityLevel.SECRET: 50,
            SecurityLevel.TOP_SECRET: 70
        }
        base_score += classification_scores.get(data_classification, 0)
        
        # Increase score for sensitive actions
        if action in ["delete", "export", "share"]:
            base_score += 20
        
        # Consider time of access (higher risk outside business hours)
        access_time = datetime.utcnow().hour
        if access_time < 6 or access_time > 22:
            base_score += 15
        
        return min(base_score, 100)
    
    async def _log_audit_event(self, 
                             event_type: AuditEventType,
                             user_id: str,
                             resource_id: Optional[str],
                             resource_type: Optional[str],
                             action: str,
                             details: Dict[str, Any],
                             ip_address: str,
                             user_agent: str,
                             session_id: Optional[str] = None,
                             risk_score: int = 0):
        """Log an audit event."""
        event = AuditEvent(
            id=str(uuid.uuid4()),
            event_type=event_type,
            user_id=user_id,
            resource_id=resource_id,
            resource_type=resource_type,
            action=action,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=datetime.utcnow(),
            session_id=session_id,
            risk_score=risk_score,
            compliance_tags=self._get_compliance_tags(event_type, details)
        )
        
        self.audit_events.append(event)
        
        # In real implementation, store in database and/or send to SIEM
        logger.info(f"Audit event: {event.event_type.value} by {user_id}")
    
    def _get_compliance_tags(self, event_type: AuditEventType, details: Dict[str, Any]) -> List[str]:
        """Get compliance tags for an event."""
        tags = []
        
        # Always include SOC2 for security events
        if event_type in [AuditEventType.LOGIN, AuditEventType.SECURITY_VIOLATION, AuditEventType.PERMISSION_CHANGE]:
            tags.append("SOC2")
        
        # GDPR for data events
        if event_type in [AuditEventType.DATA_ACCESS, AuditEventType.DATA_EXPORT]:
            tags.append("GDPR")
        
        # HIPAA if healthcare data is involved
        if details.get("data_type") == "healthcare":
            tags.append("HIPAA")
        
        return tags
    
    def _generate_gdpr_section(self, events: List[AuditEvent]) -> Dict[str, Any]:
        """Generate GDPR-specific compliance section."""
        return {
            "data_subject_requests": len([e for e in events if "data_subject_request" in e.details]),
            "data_breaches": len([e for e in events if e.event_type == AuditEventType.SECURITY_VIOLATION]),
            "consent_events": len([e for e in events if "consent" in e.details])
        }
    
    def _generate_soc2_section(self, events: List[AuditEvent]) -> Dict[str, Any]:
        """Generate SOC2-specific compliance section."""
        return {
            "access_control_events": len([e for e in events if e.event_type in [AuditEventType.LOGIN, AuditEventType.PERMISSION_CHANGE]]),
            "system_monitoring": len([e for e in events if e.event_type == AuditEventType.SYSTEM_CONFIG]),
            "incident_response": len([e for e in events if e.risk_score >= 80])
        }
    
    def _generate_hipaa_section(self, events: List[AuditEvent]) -> Dict[str, Any]:
        """Generate HIPAA-specific compliance section."""
        return {
            "phi_access_events": len([e for e in events if e.details.get("data_type") == "healthcare"]),
            "unauthorized_access": len([e for e in events if e.event_type == AuditEventType.SECURITY_VIOLATION]),
            "audit_log_integrity": True  # Simplified
        }


# Global security manager instance
security_manager: Optional[EnterpriseSecurityManager] = None


def initialize_security_manager(config: Dict[str, Any]) -> EnterpriseSecurityManager:
    """Initialize the global security manager."""
    global security_manager
    security_manager = EnterpriseSecurityManager(config)
    return security_manager


def get_security_manager() -> EnterpriseSecurityManager:
    """Get the global security manager instance."""
    if security_manager is None:
        raise RuntimeError("Security manager not initialized")
    return security_manager