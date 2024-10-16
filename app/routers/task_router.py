import logging
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.params import Depends
from sqlalchemy.orm import Session
from fastapi import status

from app.db.base import get_db
from app.models.task_models import Task, TaskStatus
from app.schemas.task_schemas import PostTaskRequest, UpdateTaskRequest, UpdateTaskStatusRequest, GetTask

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/", status_code = status.HTTP_201_CREATED)
def create_task(task: PostTaskRequest, db: Session = Depends(get_db)):
    logger.info(f"got create task request with {task}")
    task_entity = Task()
    task_entity.title = task.title
    task_entity.description = task.description
    db.add(task_entity)
    db.commit()
    db.refresh(task_entity)

    headers = {"x-task-id": str(task_entity.id)}
    return JSONResponse(content=None, headers=headers, status_code=status.HTTP_201_CREATED)

@router.get("/", response_model=List[GetTask])
def get_tasks(task_status: TaskStatus = None, db: Session = Depends(get_db)):
    logger.info(f"got request to get all tasks with status {task_status}")

    if task_status is not None:
        return db.query(Task).where(Task.status == task_status).all()

    return db.query(Task).all()

@router.get("/{task_id}", response_model=GetTask)
def get_tasks(task_id: int, db: Session = Depends(get_db)):
    logger.info(f"got request to get tasks {task_id}")
    task_from_db = db.query(Task).where(Task.id == task_id).first()
    if not task_from_db:
        raise HTTPException(status_code=404, detail=f"Task not found {task_id}")
    return task_from_db

@router.put("/{task_id}", response_model=GetTask)
def update_task(task_id: int, updated_task: UpdateTaskRequest, db: Session = Depends(get_db)):
    logger.info(f"got request to update task {task_id} with {updated_task}")

    task_from_db = db.query(Task).where(Task.id == task_id).first()

    if not task_from_db:
        raise HTTPException(status_code=404, detail=f"Task not found {task_id}")

    if updated_task.title:
        task_from_db.title = updated_task.title
    if updated_task.description:
        task_from_db.description = updated_task.description
    if updated_task.status:
        task_from_db.status = updated_task.status

    db.merge(task_from_db)
    db.commit()
    db.refresh(task_from_db)
    logger.info(f"task {task_id} updated {task_from_db}")
    return task_from_db

@router.patch("/{task_id}/status", response_model=GetTask)
def update_task_status(task_id: int, updated_task: UpdateTaskStatusRequest, db: Session = Depends(get_db)):
    logger.info(f"got request to update task status {task_id} with {updated_task}")

    task_from_db = db.query(Task).where(Task.id == task_id).first()

    if not task_from_db:
        raise HTTPException(status_code=404, detail=f"Task not found {task_id}")

    task_from_db.status = updated_task.status

    db.merge(task_from_db)
    db.commit()
    db.refresh(task_from_db)
    logger.info(f"task {task_id} updated {task_from_db}")
    return task_from_db

@router.delete("/{task_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    logger.info(f"Got request to delete task {task_id}")
    task_from_db = db.query(Task).where(Task.id == task_id).first()

    if not task_from_db:
        raise HTTPException(status_code=404, detail=f"Task not found {task_id}")

    db.delete(task_from_db)
    db.commit()

    logger.info(f"task {task_id} deleted")
    return
