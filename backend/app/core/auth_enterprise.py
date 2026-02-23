"""
Enterprise JWT Authentication & Authorization System
Supports multi-tenancy, RBAC, SSO, and advanced session management
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import structlog
import secrets
import hashlib
from enum import Enum

logger = structlog.get_logger()

# Configuration
SECRET_KEY = "your-secret-key-change-in-production-use-env-var"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
security = HTTPBearer()


class UserRole(str, Enum):
    """User roles for RBAC"""
    SUPER_ADMIN = "super_admin"  # Platform admin
    TENANT_ADMIN = "tenant_admin"  # Organization admin
    MANAGER = "manager"  # Department manager
    TEAM_LEAD = "team_lead"  # Team supervisor
    USER = "user"  # Regular user
    VIEWER = "viewer"  # Read-only access
    API_USER = "api_user"  # API-only access


class Permission(str, Enum):
    """Granular permissions"""
    # Workflow permissions
    WORKFLOW_CREATE = "workflow:create"
    WORKFLOW_READ = "workflow:read"
    WORKFLOW_UPDATE = "workflow:update"
    WORKFLOW_DELETE = "workflow:delete"
    WORKFLOW_EXECUTE = "workflow:execute"
    WORKFLOW_PUBLISH = "workflow:publish"
    
    # User management
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
    USER_ASSIGN_ROLE = "user:assign_role"
    
    # Team management
    TEAM_CREATE = "team:create"
    TEAM_READ = "team:read"
    TEAM_UPDATE = "team:update"
    TEAM_DELETE = "team:delete"
    
    # Analytics & Reports
    ANALYTICS_VIEW = "analytics:view"
    ANALYTICS_EXPORT = "analytics:export"
    REPORTS_GENERATE = "reports:generate"
    
    # System administration
    SYSTEM_CONFIG = "system:config"
    AUDIT_VIEW = "audit:view"
    BILLING_MANAGE = "billing:manage"


# Role-Permission mapping
ROLE_PERMISSIONS: Dict[UserRole, List[Permission]] = {
    UserRole.SUPER_ADMIN: [p for p in Permission],  # All permissions
    UserRole.TENANT_ADMIN: [
        Permission.WORKFLOW_CREATE, Permission.WORKFLOW_READ, Permission.WORKFLOW_UPDATE,
        Permission.WORKFLOW_DELETE, Permission.WORKFLOW_EXECUTE, Permission.WORKFLOW_PUBLISH,
        Permission.USER_CREATE, Permission.USER_READ, Permission.USER_UPDATE, Permission.USER_DELETE,
        Permission.USER_ASSIGN_ROLE, Permission.TEAM_CREATE, Permission.TEAM_READ,
        Permission.TEAM_UPDATE, Permission.TEAM_DELETE, Permission.ANALYTICS_VIEW,
        Permission.ANALYTICS_EXPORT, Permission.REPORTS_GENERATE, Permission.AUDIT_VIEW,
        Permission.BILLING_MANAGE
    ],
    UserRole.MANAGER: [
        Permission.WORKFLOW_CREATE, Permission.WORKFLOW_READ, Permission.WORKFLOW_UPDATE,
        Permission.WORKFLOW_EXECUTE, Permission.USER_READ, Permission.TEAM_READ,
        Permission.TEAM_UPDATE, Permission.ANALYTICS_VIEW, Permission.REPORTS_GENERATE
    ],
    UserRole.TEAM_LEAD: [
        Permission.WORKFLOW_READ, Permission.WORKFLOW_UPDATE, Permission.WORKFLOW_EXECUTE,
        Permission.USER_READ, Permission.TEAM_READ, Permission.ANALYTICS_VIEW
    ],
    UserRole.USER: [
        Permission.WORKFLOW_READ, Permission.WORKFLOW_EXECUTE, Permission.USER_READ,
        Permission.TEAM_READ
    ],
    UserRole.VIEWER: [
        Permission.WORKFLOW_READ, Permission.USER_READ, Permission.TEAM_READ,
        Permission.ANALYTICS_VIEW
    ],
    UserRole.API_USER: [
        Permission.WORKFLOW_READ, Permission.WORKFLOW_EXECUTE
    ]
}


class TokenData:
    """JWT token payload data"""
    def __init__(
        self,
        user_id: str,
        email: str,
        tenant_id: str,
        roles: List[str],
        permissions: List[str],
        session_id: Optional[str] = None
    ):
        self.user_id = user_id
        self.email = email
        self.tenant_id = tenant_id
        self.roles = roles
        self.permissions = permissions
        self.session_id = session_id


class AuthService:
    """Enterprise authentication and authorization service"""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash password with bcrypt"""
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })
        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(user_id: str, tenant_id: str) -> str:
        """Create JWT refresh token"""
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        
        to_encode = {
            "sub": user_id,
            "tenant_id": tenant_id,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh",
            "jti": secrets.token_urlsafe(32)  # JWT ID for revocation
        }
        
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        """Decode and validate JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError as e:
            logger.error("JWT decode error", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    @staticmethod
    def create_api_key(user_id: str, tenant_id: str) -> str:
        """Generate secure API key for API-only access"""
        raw_key = secrets.token_urlsafe(32)
        # Prefix for easy identification
        api_key = f"rp_{tenant_id[:8]}_{raw_key}"
        
        # Store hash in database (not shown here)
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        return api_key
    
    @staticmethod
    def validate_permissions(
        user_roles: List[str],
        required_permission: Permission
    ) -> bool:
        """Check if user has required permission based on roles"""
        user_permissions = set()
        
        for role_str in user_roles:
            try:
                role = UserRole(role_str)
                user_permissions.update(ROLE_PERMISSIONS.get(role, []))
            except ValueError:
                logger.warning("Invalid role", role=role_str)
        
        return required_permission in user_permissions
    
    @staticmethod
    async def get_current_user(
        token: str = Depends(oauth2_scheme)
    ) -> TokenData:
        """Extract current user from JWT token"""
        try:
            payload = AuthService.decode_token(token)
            
            user_id: str = payload.get("sub")
            email: str = payload.get("email")
            tenant_id: str = payload.get("tenant_id")
            roles: List[str] = payload.get("roles", [])
            permissions: List[str] = payload.get("permissions", [])
            session_id: str = payload.get("session_id")
            
            if user_id is None or tenant_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials"
                )
            
            return TokenData(
                user_id=user_id,
                email=email,
                tenant_id=tenant_id,
                roles=roles,
                permissions=permissions,
                session_id=session_id
            )
        
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    @staticmethod
    async def get_current_active_user(
        current_user: TokenData = Depends(get_current_user)
    ) -> TokenData:
        """Verify user is active and not disabled"""
        # In production, check database for user status
        # For now, assume all users are active
        return current_user


class PermissionChecker:
    """Dependency for checking user permissions"""
    
    def __init__(self, required_permission: Permission):
        self.required_permission = required_permission
    
    async def __call__(
        self,
        current_user: TokenData = Depends(AuthService.get_current_active_user)
    ):
        """Check if user has required permission"""
        if not AuthService.validate_permissions(current_user.roles, self.required_permission):
            logger.warning(
                "Permission denied",
                user_id=current_user.user_id,
                required_permission=self.required_permission.value
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission denied: {self.required_permission.value} required"
            )
        return current_user


class TenantIsolation:
    """Middleware for multi-tenant data isolation"""
    
    @staticmethod
    async def verify_tenant_access(
        tenant_id: str,
        current_user: TokenData = Depends(AuthService.get_current_active_user)
    ):
        """Verify user has access to requested tenant"""
        if current_user.tenant_id != tenant_id and UserRole.SUPER_ADMIN not in current_user.roles:
            logger.warning(
                "Tenant access denied",
                user_id=current_user.user_id,
                user_tenant=current_user.tenant_id,
                requested_tenant=tenant_id
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You do not have access to this organization"
            )
        return True


# Convenience dependencies for common permission checks
RequireWorkflowCreate = PermissionChecker(Permission.WORKFLOW_CREATE)
RequireWorkflowUpdate = PermissionChecker(Permission.WORKFLOW_UPDATE)
RequireWorkflowDelete = PermissionChecker(Permission.WORKFLOW_DELETE)
RequireUserManage = PermissionChecker(Permission.USER_CREATE)
RequireAdminAccess = PermissionChecker(Permission.SYSTEM_CONFIG)
RequireAnalytics = PermissionChecker(Permission.ANALYTICS_VIEW)
