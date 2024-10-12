from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum, func, DateTime
from enum import Enum

from ..db.base import Base


# Task Status Enum
class TaskStatus(str, Enum):
    TO_DO = 'To Do'
    DOING = 'Doing'
    DONE = 'Done'


# SQLAlchemy Task Model
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.TO_DO)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Auto set on insert
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # Auto update on change