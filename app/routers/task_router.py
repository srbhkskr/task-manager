import logging

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.task_models import Task
from app.schemas.task_schemas import PostTaskRequest, UpdateTaskRequest

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/")
def create_task(task: PostTaskRequest, db: Session = Depends(get_db)):
    logger.info(f"got request with {task}")
    task_entity = Task()
    task_entity.title = task.title
    task_entity.description = task.description
    db.add(task_entity)
    db.commit()
    db.refresh(task_entity)
    return task_entity

@router.get("/")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@router.put("/{task_id}")
def update_task(task_id: int, updated_task: UpdateTaskRequest, db: Session = Depends(get_db)):

    task_from_db = db.query(Task).where(Task.id == task_id).first()
    if updated_task.title:
        task_from_db.title = updated_task.title
    if updated_task.description:
        task_from_db.description = updated_task.description
    if updated_task.status:
        task_from_db.status = updated_task.status

    db.merge(task_from_db)
    db.commit()
    db.refresh(task_from_db)
    logger.info("task updated")
    return task_from_db

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):

    task_from_db = db.query(Task).where(Task.id == task_id).first()


    if not task_from_db:
        return

    db.delete(task_from_db)

    db.commit()
    db.flush()

    logger.info("task deleted")
    return
