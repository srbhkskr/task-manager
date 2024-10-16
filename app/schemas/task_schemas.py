from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.task_models import TaskStatus


class PostTaskRequest(BaseModel):
    title: str
    description: str

class UpdateTaskRequest(BaseModel):
    title: str = None
    description: str = None
    status: TaskStatus = None

class UpdateTaskStatusRequest(BaseModel):
    status: TaskStatus = None

class GetTask(BaseModel):
    id: int
    title: str
    description: str = None
    status: TaskStatus = None
    updated_at: Optional[datetime] = None
    created_at: datetime = None
