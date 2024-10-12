from pydantic import BaseModel, Field

from app.models.task_models import TaskStatus


class PostTaskRequest(BaseModel):
    title: str
    description: str

class UpdateTaskRequest(BaseModel):
    title: str = None
    description: str = None
    status: TaskStatus = None
