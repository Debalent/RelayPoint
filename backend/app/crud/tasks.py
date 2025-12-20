from sqlalchemy.orm import Session
from app.models import task as task_model


def create_task(db: Session, *, id: str, title: str, description: str = None, role: str = None, priority: str = None, department: str = None, guest_room: str = None, guest_name: str = None, raw: dict = None):
    obj = task_model.Task(
        id=id,
        title=title,
        description=description,
        role=role,
        priority=priority,
        department=department,
        guest_room=guest_room,
        guest_name=guest_name,
        raw=raw
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_task(db: Session, *, task_id: str):
    return db.query(task_model.Task).filter_by(id=task_id).first()


def list_tasks(db: Session, *, department: str = None):
    q = db.query(task_model.Task)
    if department:
        q = q.filter_by(department=department)
    return q.all()