import datetime
from enum import Enum

from sqlalchemy import Integer, String, Enum as SQLAlchemyEnum, func, DateTime
from sqlalchemy.orm import mapped_column, Mapped

from ..db.base import Base


class TaskStatus(str, Enum):
    TO_DO = 'ToDo'
    DOING = 'Doing'
    DONE = 'Done'


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String)
    status: Mapped[TaskStatus] = mapped_column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.TO_DO)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
