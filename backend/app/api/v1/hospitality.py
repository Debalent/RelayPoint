"""
Hospitality Operations API
Addresses survey feedback for hospitality workflow automation:

Key Requirements from Survey:
- 100% experience communication delays between departments
- 79% need multilingual support  
- 64% need accessibility features
- 50% report tasks get missed/duplicated "sometimes"
- 86% want easy, time-saving, mobile-friendly tools

This API provides:
1. Real-time department communication
2. Task accountability with auto-escalation
3. Multilingual support
4. Mobile-optimized endpoints
5. Voice note integration
6. Shift handoff management
7. Guest service tracking
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query, Body
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
import json
import asyncio
from enum import Enum

from app.core.hospitality_config import (
    HospitalityTask, 
    DepartmentAlert, 
    ShiftHandoff, 
    HospitalityRole, 
    TaskPriority, 
    TaskStatus,
    LanguageSupport,
    hospitality_config
)
from app.core.websocket_manager_elite import websocket_manager
from app.core.security import get_current_user
from app.db import get_db
from app.models.user import User

router = APIRouter(prefix="/api/v1/hospitality", tags=["hospitality"])

# Request/Response Models
class TaskCreateRequest(BaseModel):
    title: str
    description: str
    role: HospitalityRole
    priority: TaskPriority = TaskPriority.MEDIUM
    department: str
    guest_room: Optional[str] = None
    guest_name: Optional[str] = None
    estimated_duration: Optional[int] = None
    due_at: Optional[datetime] = None
    shift: str = "current"
    guest_impact: bool = False

class TaskUpdateRequest(BaseModel):
    status: Optional[TaskStatus] = None
    assigned_to: Optional[str] = None
    handoff_notes: Optional[str] = None
    completion_notes: Optional[str] = None

class AlertCreateRequest(BaseModel):
    message: str
    from_department: str
    to_department: str
    priority: TaskPriority = TaskPriority.MEDIUM
    alert_type: str
    auto_escalate_after: int = 5  # minutes

class VoiceNoteRequest(BaseModel):
    task_id: str
    audio_data: str  # Base64 encoded audio
    language: LanguageSupport = LanguageSupport.ENGLISH

class QuickMessageRequest(BaseModel):
    message_type: str
    from_department: str
    to_department: str
    additional_context: Optional[str] = None
    language: LanguageSupport = LanguageSupport.ENGLISH

class ShiftHandoffRequest(BaseModel):
    from_shift: str
    to_shift: str
    department: str
    active_tasks: List[str]
    guest_issues: List[Dict[str, Any]]
    maintenance_alerts: List[str]
    staffing_notes: str
    inventory_concerns: List[str]
    special_instructions: str

class StaffStatusResponse(BaseModel):
    user_id: str
    name: str
    role: HospitalityRole
    department: str
    current_shift: str
    active_tasks: int
    status: str  # "available", "busy", "break", "offline"
    last_seen: datetime

# Task Management Endpoints
@router.get("/tasks", response_model=List[HospitalityTask])
async def get_tasks(
    role: Optional[HospitalityRole] = None,
    department: Optional[str] = None,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    shift: Optional[str] = None,
    guest_impact_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get tasks filtered by various criteria
    Addresses survey feedback: "No way to see what's already been done"
    """
    # In real implementation, this would query the database
    # For demo, returning sample data based on filters
    
    sample_tasks = [
        {
            "id": "task_001",
            "title": "Guest Checkout - Room 312",
            "description": "Process checkout for VIP guest, ensure satisfaction survey",
            "role": HospitalityRole.FRONT_DESK,
            "priority": TaskPriority.HIGH,
            "status": TaskStatus.PENDING,
            "department": "front_desk",
            "guest_room": "312",
            "guest_name": "Johnson, Robert",
            "estimated_duration": 15,
            "created_at": datetime.now(),
            "shift": "morning",
            "guest_impact": True,
            "communication_log": [],
            "voice_notes": []
        },
        {
            "id": "task_002", 
            "title": "Maintenance Request - AC Unit Room 205",
            "description": "Guest reports AC making loud noise, investigate and repair",
            "role": HospitalityRole.MAINTENANCE,
            "priority": TaskPriority.URGENT,
            "status": TaskStatus.ESCALATED,
            "department": "maintenance",
            "guest_room": "205",
            "estimated_duration": 45,
            "created_at": datetime.now() - timedelta(minutes=30),
            "escalated_at": datetime.now() - timedelta(minutes=5),
            "shift": "morning",
            "guest_impact": True,
            "communication_log": [
                {
                    "timestamp": datetime.now() - timedelta(minutes=25),
                    "from": "front_desk",
                    "message": "Guest called about loud AC noise",
                    "priority": "urgent"
                }
            ],
            "voice_notes": []
        }
    ]
    
    # Apply filters
    filtered_tasks = sample_tasks
    if role:
        filtered_tasks = [t for t in filtered_tasks if t["role"] == role]
    if department:
        filtered_tasks = [t for t in filtered_tasks if t["department"] == department]
    if status:
        filtered_tasks = [t for t in filtered_tasks if t["status"] == status]
    if priority:
        filtered_tasks = [t for t in filtered_tasks if t["priority"] == priority]
    if guest_impact_only:
        filtered_tasks = [t for t in filtered_tasks if t["guest_impact"]]
    
    return filtered_tasks

@router.post("/tasks", response_model=HospitalityTask)
async def create_task(
    task_data: TaskCreateRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new hospitality task with auto-escalation
    Addresses survey feedback: Need for task accountability
    """
    task = HospitalityTask(
        id=f"task_{datetime.now().timestamp()}",
        title=task_data.title,
        description=task_data.description,
        role=task_data.role,
        priority=task_data.priority,
        department=task_data.department,
        guest_room=task_data.guest_room,
        guest_name=task_data.guest_name,
        estimated_duration=task_data.estimated_duration,
        created_at=datetime.now(),
        due_at=task_data.due_at,
        shift=task_data.shift,
        guest_impact=task_data.guest_impact
    )
    
    # Schedule auto-escalation based on priority
    escalation_rules = hospitality_config.ESCALATION_RULES[task_data.priority]
    if escalation_rules["first_escalation"] > 0:
        background_tasks.add_task(
            schedule_task_escalation,
            task.id,
            escalation_rules["first_escalation"]
        )
    
    # Send real-time notification to department
    await websocket_manager.send_to_group(
        f"department_{task_data.department}",
        {
            "type": "new_task",
            "task": task.dict(),
            "priority": task_data.priority.value
        }
    )
    
    return task

@router.put("/tasks/{task_id}", response_model=HospitalityTask)
async def update_task(
    task_id: str,
    task_update: TaskUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update task status with real-time notifications
    Addresses survey feedback: Need for task completion tracking
    """
    # In real implementation, fetch from database
    # For demo, create updated task
    
    updated_task = HospitalityTask(
        id=task_id,
        title="Updated Task",
        description="Task description",
        role=HospitalityRole.FRONT_DESK,
        priority=TaskPriority.MEDIUM,
        status=task_update.status or TaskStatus.PENDING,
        department="front_desk",
        created_at=datetime.now()
    )
    
    if task_update.status == TaskStatus.COMPLETED:
        updated_task.completed_at = datetime.now()
    
    # Send real-time update to all relevant departments
    await websocket_manager.broadcast({
        "type": "task_updated",
        "task_id": task_id,
        "status": task_update.status,
        "updated_by": current_user.email,
        "timestamp": datetime.now().isoformat()
    })
    
    return updated_task

# Department Communication
@router.get("/alerts", response_model=List[DepartmentAlert])
async def get_department_alerts(
    department: Optional[str] = None,
    priority: Optional[TaskPriority] = None,
    unacknowledged_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get department alerts with escalation tracking
    Addresses survey feedback: Communication gaps between departments
    """
    sample_alerts = [
        {
            "id": "alert_001",
            "message": "Guest in room 312 requesting immediate assistance with luggage",
            "from_department": "front_desk",
            "to_department": "housekeeping",
            "priority": TaskPriority.HIGH,
            "alert_type": "guest_request",
            "created_at": datetime.now() - timedelta(minutes=5),
            "escalation_count": 1
        },
        {
            "id": "alert_002",
            "message": "Low inventory: Towels running low, need restocking ASAP",
            "from_department": "housekeeping", 
            "to_department": "management",
            "priority": TaskPriority.MEDIUM,
            "alert_type": "inventory_low",
            "created_at": datetime.now() - timedelta(minutes=15),
            "escalation_count": 0
        }
    ]
    
    filtered_alerts = sample_alerts
    if department:
        filtered_alerts = [a for a in filtered_alerts if a["to_department"] == department]
    if unacknowledged_only:
        filtered_alerts = [a for a in filtered_alerts if "acknowledged_at" not in a]
    
    return filtered_alerts

@router.post("/alerts", response_model=DepartmentAlert)
async def create_department_alert(
    alert_data: AlertCreateRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create department alert with auto-escalation
    Addresses survey feedback: Need for alert system with follow-up
    """
    alert = DepartmentAlert(
        id=f"alert_{datetime.now().timestamp()}",
        message=alert_data.message,
        from_department=alert_data.from_department,
        to_department=alert_data.to_department,
        priority=alert_data.priority,
        alert_type=alert_data.alert_type,
        created_at=datetime.now(),
        auto_escalate_after=alert_data.auto_escalate_after
    )
    
    # Send immediate notification to target department
    await websocket_manager.send_to_group(
        f"department_{alert_data.to_department}",
        {
            "type": "new_alert",
            "alert": alert.dict(),
            "from": alert_data.from_department
        }
    )
    
    # Schedule auto-escalation
    background_tasks.add_task(
        schedule_alert_escalation,
        alert.id,
        alert_data.auto_escalate_after
    )
    
    return alert

@router.post("/quick-message")
async def send_quick_message(
    message_data: QuickMessageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send pre-defined quick messages between departments
    Addresses survey feedback: Need for fast communication
    """
    quick_messages = hospitality_config.QUICK_MESSAGES[message_data.language.value]
    
    if message_data.message_type in quick_messages:
        message_text = quick_messages[message_data.message_type]
        if message_data.additional_context:
            message_text += f" - {message_data.additional_context}"
    else:
        message_text = message_data.message_type
    
    # Send real-time message
    await websocket_manager.send_to_group(
        f"department_{message_data.to_department}",
        {
            "type": "quick_message",
            "message": message_text,
            "from": message_data.from_department,
            "from_user": current_user.email,
            "timestamp": datetime.now().isoformat(),
            "language": message_data.language.value
        }
    )
    
    return {"status": "sent", "message": message_text}

# Voice Integration
@router.post("/voice-note")
async def process_voice_note(
    voice_data: VoiceNoteRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Process voice note and convert to text
    Addresses survey feedback: Voice-to-text for quick notes
    """
    # In real implementation, this would use speech recognition service
    # For demo, return mock transcription
    
    mock_transcriptions = {
        "en": "Task completed successfully, guest was satisfied with service",
        "es": "Tarea completada exitosamente, el huésped quedó satisfecho con el servicio", 
        "fr": "Tâche terminée avec succès, le client était satisfait du service"
    }
    
    transcription = mock_transcriptions.get(voice_data.language.value, "Voice note processed")
    
    # Add to task communication log
    # In real implementation, update database
    
    return {
        "transcription": transcription,
        "language": voice_data.language.value,
        "confidence": 0.95,
        "task_id": voice_data.task_id
    }

# Shift Management
@router.post("/shift-handoff", response_model=ShiftHandoff)
async def create_shift_handoff(
    handoff_data: ShiftHandoffRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create structured shift handoff
    Addresses survey feedback: Better shift information transfer
    """
    handoff = ShiftHandoff(
        id=f"handoff_{datetime.now().timestamp()}",
        from_shift=handoff_data.from_shift,
        to_shift=handoff_data.to_shift,
        department=handoff_data.department,
        handoff_time=datetime.now(),
        active_tasks=handoff_data.active_tasks,
        guest_issues=handoff_data.guest_issues,
        maintenance_alerts=handoff_data.maintenance_alerts,
        staffing_notes=handoff_data.staffing_notes,
        inventory_concerns=handoff_data.inventory_concerns,
        special_instructions=handoff_data.special_instructions,
        created_by=current_user.email
    )
    
    # Notify incoming shift
    await websocket_manager.send_to_group(
        f"department_{handoff_data.department}",
        {
            "type": "shift_handoff",
            "handoff": handoff.dict(),
            "from_shift": handoff_data.from_shift,
            "to_shift": handoff_data.to_shift
        }
    )
    
    return handoff

@router.get("/shift-handoff/{department}")
async def get_latest_shift_handoff(
    department: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get the latest shift handoff for a department"""
    # In real implementation, query database for latest handoff
    return {
        "message": f"Latest shift handoff for {department}",
        "handoff_time": datetime.now() - timedelta(hours=8),
        "notes": "All tasks completed, no outstanding issues"
    }

# Staff Status and Communication
@router.get("/staff-status", response_model=List[StaffStatusResponse])
async def get_staff_status(
    department: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get real-time staff availability status
    Addresses survey feedback: Need to know staffing levels
    """
    sample_staff = [
        {
            "user_id": "staff_001",
            "name": "Maria Rodriguez",
            "role": HospitalityRole.HOUSEKEEPING,
            "department": "housekeeping",
            "current_shift": "morning",
            "active_tasks": 3,
            "status": "busy",
            "last_seen": datetime.now() - timedelta(minutes=2)
        },
        {
            "user_id": "staff_002",
            "name": "James Chen",
            "role": HospitalityRole.MAINTENANCE,
            "department": "maintenance", 
            "current_shift": "morning",
            "active_tasks": 1,
            "status": "available",
            "last_seen": datetime.now() - timedelta(minutes=1)
        }
    ]
    
    if department:
        sample_staff = [s for s in sample_staff if s["department"] == department]
    
    return sample_staff

# Guest Service Tracking
@router.get("/guest-requests")
async def get_guest_requests(
    room: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[TaskPriority] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Track guest service requests across departments
    Addresses survey feedback: No system for tracking guest service requests
    """
    sample_requests = [
        {
            "id": "req_001",
            "guest_name": "Smith, John",
            "room": "312",
            "request_type": "extra_towels",
            "description": "Guest requested extra towels and bathrobes",
            "priority": TaskPriority.MEDIUM,
            "status": "pending",
            "assigned_department": "housekeeping",
            "created_at": datetime.now() - timedelta(minutes=10),
            "requested_completion": datetime.now() + timedelta(minutes=30)
        },
        {
            "id": "req_002", 
            "guest_name": "Johnson, Sarah",
            "room": "205",
            "request_type": "maintenance",
            "description": "Guest reports bathroom faucet dripping",
            "priority": TaskPriority.HIGH,
            "status": "in_progress",
            "assigned_department": "maintenance",
            "created_at": datetime.now() - timedelta(minutes=45),
            "estimated_completion": datetime.now() + timedelta(minutes=15)
        }
    ]
    
    filtered_requests = sample_requests
    if room:
        filtered_requests = [r for r in filtered_requests if r["room"] == room]
    if status:
        filtered_requests = [r for r in filtered_requests if r["status"] == status]
    
    return filtered_requests

# Analytics and Reporting
@router.get("/analytics/task-completion")
async def get_task_completion_analytics(
    department: Optional[str] = None,
    date_range: int = Query(7, description="Days to analyze"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get task completion analytics
    Addresses survey feedback: Need for performance tracking
    """
    return {
        "period": f"Last {date_range} days",
        "department": department or "all",
        "total_tasks": 156,
        "completed_on_time": 142,
        "completion_rate": 91.0,
        "average_completion_time": 45,  # minutes
        "escalation_rate": 5.8,
        "guest_satisfaction_score": 4.7,
        "department_breakdown": {
            "housekeeping": {"completion_rate": 94.2, "avg_time": 32},
            "maintenance": {"completion_rate": 87.5, "avg_time": 68},
            "front_desk": {"completion_rate": 96.1, "avg_time": 18},
            "banquet_events": {"completion_rate": 89.3, "avg_time": 52}
        }
    }

# Background Tasks
async def schedule_task_escalation(task_id: str, escalation_minutes: int):
    """Schedule task escalation after specified time"""
    await asyncio.sleep(escalation_minutes * 60)
    
    # Check if task is still pending and escalate
    await websocket_manager.broadcast({
        "type": "task_escalated",
        "task_id": task_id,
        "escalation_time": datetime.now().isoformat(),
        "message": f"Task {task_id} automatically escalated after {escalation_minutes} minutes"
    })

async def schedule_alert_escalation(alert_id: str, escalation_minutes: int):
    """Schedule alert escalation after specified time"""
    await asyncio.sleep(escalation_minutes * 60)
    
    # Send escalation notification
    await websocket_manager.broadcast({
        "type": "alert_escalated", 
        "alert_id": alert_id,
        "escalation_time": datetime.now().isoformat(),
        "message": f"Alert {alert_id} escalated to management"
    })

# Translation endpoint
@router.post("/translate")
async def translate_text(
    text: str = Body(..., embed=True),
    target_language: LanguageSupport = Body(..., embed=True),
    source_language: LanguageSupport = Body(LanguageSupport.ENGLISH, embed=True)
):
    """
    Translate text between supported languages
    Addresses survey feedback: 79% need multilingual support
    """
    # Mock translation - in real implementation, use translation service
    translations_map = {
        ("en", "es"): {
            "Guest waiting": "Huésped esperando",
            "Task completed": "Tarea completada",
            "Need assistance": "Necesito ayuda",
            "Maintenance required": "Se requiere mantenimiento"
        },
        ("en", "fr"): {
            "Guest waiting": "Client en attente",
            "Task completed": "Tâche terminée", 
            "Need assistance": "Besoin d'aide",
            "Maintenance required": "Maintenance nécessaire"
        }
    }
    
    translation_key = (source_language.value, target_language.value)
    translated_text = translations_map.get(translation_key, {}).get(text, f"[{target_language.value}] {text}")
    
    return {
        "original_text": text,
        "translated_text": translated_text,
        "source_language": source_language.value,
        "target_language": target_language.value,
        "confidence": 0.95
    }