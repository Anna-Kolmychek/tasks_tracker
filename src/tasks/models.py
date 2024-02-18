from datetime import date
from typing import Optional, List

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Date, MetaData
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base
from src.tasks.schemas import TaskStatus

metadata_task = MetaData()


class Task(Base):
    __tablename__ = "task"

    # metadata = metadata_task

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(String, default=None)
    status: Mapped[Optional[TaskStatus]] = mapped_column(Enum(TaskStatus), default=TaskStatus.new)
    deadline: Mapped[Optional[date]] = mapped_column(Date, default=None)

    parent_task_id: Mapped[Optional[int]] = mapped_column(ForeignKey('task.id'), default=None)
    maker_id: Mapped[Optional[int]] = mapped_column(ForeignKey('user_account.id'), default=None)
    maker_position_id: Mapped[Optional[int]] = mapped_column(ForeignKey('job_position.id'), default=None)

    child_tasks: Mapped[List['Task']] = relationship(remote_side=[parent_task_id])
    maker: Mapped['User'] = relationship(back_populates='tasks')
    maker_position: Mapped['Position'] = relationship(back_populates='tasks')
