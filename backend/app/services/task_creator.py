from app.core.websocket_manager import WebSocketManager
from app.core.hospitality_config import HospitalityTask, TaskPriority, HospitalityRole
from datetime import datetime
from sqlalchemy.orm import Session
from app.crud import tasks as tasks_crud

# Use existing websocket_manager instance
from app.api.v1.hospitality import websocket_manager

async def create_turnover_task(db: Session, property_id: int, room_number: str, room_id: str):
    """Create a basic turnover task, persist to DB and broadcast to housekeeping group."""
    task_id = f"task_{datetime.now().timestamp()}"
    task = HospitalityTask(
        id=task_id,
        title=f"Turnover: Room {room_number}",
        description=f"Turnover after checkout for room {room_number}",
        role=HospitalityRole.HOUSEKEEPING,
        priority=TaskPriority.HIGH,
        department="housekeeping",
        guest_room=room_number,
        created_at=datetime.now(),
        due_at=None,
        shift=None,
        guest_impact=False
    )

    # Persist task
    tasks_crud.create_task(db, id=task.id, title=task.title, description=task.description, role=task.role.value if hasattr(task.role, 'value') else str(task.role), priority=task.priority.value if hasattr(task.priority, 'value') else str(task.priority), department=task.department, guest_room=task.guest_room, guest_name=task.guest_name, raw=task.dict())

    # Broadcast to housekeeping group
    await websocket_manager.send_to_group(
        "department_housekeeping",
        {
            "type": "new_task",
            "task": task.dict(),
            "priority": TaskPriority.HIGH.value
        }
    )

    return task.dict()