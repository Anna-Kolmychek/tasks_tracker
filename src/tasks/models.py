from datetime import date
from typing import Optional

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base
from src.tasks.schemas import TaskStatus
from src.users.models import User, Position


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(String, default=None)
    status: Mapped[Optional[TaskStatus]] = mapped_column(Enum(TaskStatus), default=None)
    deadline: Mapped[Optional[date]] = mapped_column(Date, default=None)

    parent_task_id: Mapped[Optional[int]] = mapped_column(ForeignKey('task.id'), default=None)
    maker_id: Mapped[Optional[int]] = mapped_column(ForeignKey('user_account.id'), default=None)
    maker_position_id: Mapped[Optional[int]] = mapped_column(ForeignKey('job_position.id'), default=None)

    parent_task: Mapped['Task'] = relationship(back_populates='child_task')
    maker: Mapped['User'] = relationship(back_populates='tasks')
    maker_position: Mapped['Position'] = relationship(back_populates='tasks')
