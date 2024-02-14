from src.users.schemas import User
from src.tasks.schemas import Task


class UserWithTasks(User):
    tasks: list[Task]
