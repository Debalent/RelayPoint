"""
RelayPoint Elite - Hospitality Operations Configuration
Specifically designed to address hospitality workforce feedback and pain points

This configuration addresses key findings from hospitality survey:
- 79% need multilingual support
- 64% need accessibility features (large text, screen reader)
- 100% experience communication delays between departments
- 50% report tasks get missed/duplicated "sometimes"
- 86% want "all the above" features (easy to use, saves time, mobile-friendly, management support)

Survey insights implemented:
1. Real-time department communication
2. Task accountability and tracking
3. Multilingual interface support
4. Mobile-first responsive design
5. Voice-to-text for quick notes
6. Automated alerts and reminders
7. Shift handoff management
8. Guest service request tracking
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

class HospitalityRole(str, Enum):
    FRONT_DESK = "front_desk"
    HOUSEKEEPING = "housekeeping"
    MAINTENANCE = "maintenance"
    BANQUET_EVENT = "banquet_event"
    ADMIN_MANAGER = "admin_manager"
    BAR_RESTAURANT = "bar_restaurant"
    SECURITY = "security"
    CONCIERGE = "concierge"

class TaskPriority(str, Enum):
    URGENT = "urgent"           # Guest-facing, immediate attention
    HIGH = "high"              # Same-shift completion required
    MEDIUM = "medium"          # Next shift handoff acceptable
    LOW = "low"               # Can be scheduled for later

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ESCALATED = "escalated"
    CANCELLED = "cancelled"

class CommunicationChannel(str, Enum):
    MOBILE_APP = "mobile_app"
    WALKIE_TALKIE = "walkie_talkie"
    TEXT_MESSAGE = "text_message"
    PAPER_LOG = "paper_log"
    VERBAL = "verbal"

class LanguageSupport(str, Enum):
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    CHINESE = "zh"
    KOREAN = "ko"
    ARABIC = "ar"
    PORTUGUESE = "pt"
    RUSSIAN = "ru"

class AccessibilityFeature(str, Enum):
    LARGE_TEXT = "large_text"
    HIGH_CONTRAST = "high_contrast"
    SCREEN_READER = "screen_reader"
    VOICE_COMMANDS = "voice_commands"
    SIMPLIFIED_UI = "simplified_ui"

class HospitalityTask(BaseModel):
    """Enhanced task model for hospitality operations"""
    id: str
    title: str
    description: str
    role: HospitalityRole
    priority: TaskPriority
    status: TaskStatus = TaskStatus.PENDING
    assigned_to: Optional[str] = None
    department: str
    guest_room: Optional[str] = None
    guest_name: Optional[str] = None
    estimated_duration: Optional[int] = Field(None, description="Duration in minutes")
    created_at: datetime
    due_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    escalated_at: Optional[datetime] = None
    shift: str  # "morning", "afternoon", "evening", "overnight"
    
    # Communication tracking
    communication_log: List[Dict[str, Any]] = Field(default_factory=list)
    handoff_notes: Optional[str] = None
    voice_notes: Optional[List[str]] = Field(default_factory=list)
    
    # Guest service tracking
    guest_impact: bool = False
    service_recovery: bool = False
    guest_satisfaction_score: Optional[int] = None

class DepartmentAlert(BaseModel):
    """Alert system for cross-department communication"""
    id: str
    message: str
    from_department: str
    to_department: str
    priority: TaskPriority
    alert_type: str  # "guest_request", "maintenance_needed", "inventory_low", "staff_needed"
    created_at: datetime
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    escalation_count: int = 0
    auto_escalate_after: int = 5  # minutes

class ShiftHandoff(BaseModel):
    """Structured shift handoff system"""
    id: str
    from_shift: str
    to_shift: str
    department: str
    handoff_time: datetime
    
    # Key information transfer
    active_tasks: List[str]  # Task IDs
    guest_issues: List[Dict[str, Any]]
    maintenance_alerts: List[str]
    staffing_notes: str
    inventory_concerns: List[str]
    special_instructions: str
    
    # Acknowledgment
    created_by: str
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None

class HospitalityWorkflowConfig:
    """Configuration optimized for hospitality operations based on survey feedback"""
    
    # Language and accessibility settings
    SUPPORTED_LANGUAGES = {
        LanguageSupport.ENGLISH: {
            "name": "English",
            "code": "en",
            "rtl": False
        },
        LanguageSupport.SPANISH: {
            "name": "Español",
            "code": "es", 
            "rtl": False
        },
        LanguageSupport.FRENCH: {
            "name": "Français",
            "code": "fr",
            "rtl": False
        },
        LanguageSupport.CHINESE: {
            "name": "中文",
            "code": "zh",
            "rtl": False
        },
        LanguageSupport.KOREAN: {
            "name": "한국어",
            "code": "ko",
            "rtl": False
        },
        LanguageSupport.ARABIC: {
            "name": "العربية",
            "code": "ar",
            "rtl": True
        }
    }
    
    # Accessibility configurations
    ACCESSIBILITY_OPTIONS = {
        AccessibilityFeature.LARGE_TEXT: {
            "font_scale": 1.4,
            "line_height": 1.6,
            "button_padding": "16px"
        },
        AccessibilityFeature.HIGH_CONTRAST: {
            "background": "#000000",
            "text": "#FFFFFF",
            "accent": "#FFD700"
        },
        AccessibilityFeature.SCREEN_READER: {
            "aria_labels": True,
            "semantic_markup": True,
            "skip_links": True
        },
        AccessibilityFeature.VOICE_COMMANDS: {
            "speech_recognition": True,
            "voice_shortcuts": True,
            "audio_feedback": True
        }
    }
    
    # Department configuration based on survey roles
    DEPARTMENTS = {
        "front_desk": {
            "name": "Front Desk",
            "primary_role": HospitalityRole.FRONT_DESK,
            "communication_priority": "high",
            "guest_facing": True
        },
        "housekeeping": {
            "name": "Housekeeping", 
            "primary_role": HospitalityRole.HOUSEKEEPING,
            "communication_priority": "medium",
            "guest_facing": True
        },
        "maintenance": {
            "name": "Maintenance",
            "primary_role": HospitalityRole.MAINTENANCE,
            "communication_priority": "high",
            "guest_facing": False
        },
        "banquet_events": {
            "name": "Banquet & Events",
            "primary_role": HospitalityRole.BANQUET_EVENT,
            "communication_priority": "medium",
            "guest_facing": True
        },
        "management": {
            "name": "Management",
            "primary_role": HospitalityRole.ADMIN_MANAGER,
            "communication_priority": "highest",
            "guest_facing": True
        },
        "bar_restaurant": {
            "name": "Bar & Restaurant",
            "primary_role": HospitalityRole.BAR_RESTAURANT,
            "communication_priority": "high",
            "guest_facing": True
        }
    }
    
    # Alert escalation based on survey feedback about missed tasks
    ESCALATION_RULES = {
        TaskPriority.URGENT: {
            "initial_alert": 0,      # Immediate
            "first_escalation": 5,   # 5 minutes
            "manager_escalation": 10, # 10 minutes
            "repeat_interval": 5     # Every 5 minutes after
        },
        TaskPriority.HIGH: {
            "initial_alert": 0,
            "first_escalation": 15,  # 15 minutes
            "manager_escalation": 30, # 30 minutes
            "repeat_interval": 10
        },
        TaskPriority.MEDIUM: {
            "initial_alert": 0,
            "first_escalation": 30,  # 30 minutes
            "manager_escalation": 60, # 1 hour
            "repeat_interval": 15
        },
        TaskPriority.LOW: {
            "initial_alert": 0,
            "first_escalation": 120, # 2 hours
            "manager_escalation": 240, # 4 hours
            "repeat_interval": 30
        }
    }
    
    # Mobile-first design settings (86% wanted mobile-friendly)
    MOBILE_CONFIG = {
        "touch_target_min_size": "44px",
        "font_size_min": "16px",
        "offline_mode": True,
        "push_notifications": True,
        "location_services": True,
        "camera_integration": True,  # For incident reporting
        "voice_input": True
    }
    
    # Communication templates addressing survey feedback
    QUICK_MESSAGES = {
        "en": {
            "task_completed": "Task completed ✓",
            "need_assistance": "Need assistance with this task",
            "guest_waiting": "Guest waiting - please prioritize",
            "maintenance_required": "Maintenance required in room",
            "housekeeping_needed": "Housekeeping needed",
            "front_desk_call": "Please call front desk",
            "shift_handoff": "Ready for shift handoff",
            "all_clear": "All tasks completed - all clear"
        },
        "es": {
            "task_completed": "Tarea completada ✓",
            "need_assistance": "Necesito ayuda con esta tarea",
            "guest_waiting": "Huésped esperando - por favor priorizar",
            "maintenance_required": "Se requiere mantenimiento en habitación",
            "housekeeping_needed": "Se necesita limpieza",
            "front_desk_call": "Por favor llamar recepción",
            "shift_handoff": "Listo para cambio de turno",
            "all_clear": "Todas las tareas completadas"
        }
    }
    
    # Task templates addressing common hospitality workflows
    TASK_TEMPLATES = {
        "guest_checkout": {
            "title": "Guest Checkout - Room {room}",
            "department": "housekeeping",
            "priority": TaskPriority.HIGH,
            "estimated_duration": 30,
            "checklist": [
                "Check guest satisfaction",
                "Process checkout payment",
                "Schedule housekeeping",
                "Update room status",
                "Handle any guest requests"
            ]
        },
        "maintenance_request": {
            "title": "Maintenance Request - {issue}",
            "department": "maintenance", 
            "priority": TaskPriority.MEDIUM,
            "estimated_duration": 45,
            "auto_escalate": True
        },
        "event_setup": {
            "title": "Event Setup - {event_name}",
            "department": "banquet_events",
            "priority": TaskPriority.HIGH,
            "estimated_duration": 120,
            "requires_coordination": ["housekeeping", "maintenance", "bar_restaurant"]
        },
        "guest_complaint": {
            "title": "Guest Complaint - Room {room}",
            "department": "front_desk",
            "priority": TaskPriority.URGENT,
            "estimated_duration": 20,
            "service_recovery": True,
            "requires_follow_up": True
        }
    }

# Utility functions for hospitality-specific workflows
class HospitalityWorkflowUtils:
    
    @staticmethod
    def calculate_shift_times():
        """Calculate shift boundaries for proper handoff timing"""
        shifts = {
            "morning": {"start": "06:00", "end": "14:00"},
            "afternoon": {"start": "14:00", "end": "22:00"}, 
            "overnight": {"start": "22:00", "end": "06:00"}
        }
        return shifts
    
    @staticmethod
    def get_department_alerts(department: str, priority: TaskPriority = None) -> List[DepartmentAlert]:
        """Get active alerts for a department"""
        # Implementation would fetch from database
        pass
    
    @staticmethod
    def create_shift_handoff(from_shift: str, to_shift: str, department: str) -> ShiftHandoff:
        """Create structured shift handoff"""
        # Implementation would create handoff with current state
        pass
    
    @staticmethod
    def translate_message(message: str, target_language: LanguageSupport) -> str:
        """Translate message to target language"""
        # Implementation would use translation service
        pass
    
    @staticmethod
    def voice_to_text(audio_data: bytes, language: LanguageSupport = LanguageSupport.ENGLISH) -> str:
        """Convert voice note to text"""
        # Implementation would use speech recognition
        pass
    
    @staticmethod
    def send_department_alert(
        message: str,
        from_dept: str,
        to_dept: str,
        priority: TaskPriority,
        alert_type: str
    ) -> DepartmentAlert:
        """Send alert between departments with auto-escalation"""
        alert = DepartmentAlert(
            id=f"alert_{datetime.now().timestamp()}",
            message=message,
            from_department=from_dept,
            to_department=to_dept,
            priority=priority,
            alert_type=alert_type,
            created_at=datetime.now()
        )
        
        # Schedule auto-escalation based on priority
        escalation_rules = HospitalityWorkflowConfig.ESCALATION_RULES[priority]
        # Implementation would schedule escalation tasks
        
        return alert

# Configuration instance
hospitality_config = HospitalityWorkflowConfig()