from datetime import date

from pydantic import BaseModel

from src.users.schemas import User
from src.tasks.schemas import Task


class UserWithTasks(User):
    tasks: list[Task]


class ImportantTasks(BaseModel):
    task: Task
    deadline: date
    possible_makers: list[str]
