from datetime import date
from enum import Enum

from pydantic import BaseModel


class TaskStatus(Enum):
    new = 'new'
    in_work = 'in work'
    closed = 'closed'


class TaskOptioanlPart(BaseModel):
    description: str | None = None
    status: TaskStatus | None = TaskStatus.new
    parent_task_id: int | None = None
    maker_id: int | None = None
    maker_position_id: int | None = None
    deadline: date | None = None


class TaskCreate(TaskOptioanlPart):
    title: str


class TaskUpdate(TaskOptioanlPart):
    title: str

class TaskPartialUpdate(TaskOptioanlPart):
    title: str | None = None


class Task(TaskOptioanlPart):
    id: int
    title: str

