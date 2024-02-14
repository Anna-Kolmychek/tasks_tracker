from sqlalchemy.orm import Session, selectinload

from src.tasks.schemas import TaskStatus
from src.users import models as models_user
from src.tasks import models as models_task


def count_open_tasks(user: models_user.User):
    return sum(1 for task in user.tasks if task.status != TaskStatus.closed)


def get_db_important_tasks(db: Session):
    important_tasks = []
    db_tasks = (db.query(models_task.Task)
                .options(selectinload(models_task.Task.child_tasks))
                .where(models_task.Task.status == TaskStatus.new)
                .all())

    for task in db_tasks:
        is_important_task = False
        for child_task in task.child_tasks:
            if child_task.status == TaskStatus.in_work:
                is_important_task = True
                break
        if is_important_task:
            important_tasks.append(task)

    return important_tasks


def get_free_user_by_position(db_all_users, position_id: int, db: Session):
    db_users = (db_all_users
                .where(models_user.User.position_id == position_id)
                .all())

    db_users.sort(key=count_open_tasks)
    min_count = count_open_tasks(db_users[0])

    free_db_users = [user for user in db_users if count_open_tasks(user) == min_count]

    return free_db_users


def get_child_tasks_makers_by_max_count_tasks(db_all_users, max_count_tasks: int, tasks: list[models_task.Task]):
    possible_users_id = [task.maker_id for task in tasks if task.status == TaskStatus.in_work]
    possible_db_users = (db_all_users
                         .where(models_user.User.id.in_(possible_users_id))
                         .all())
    child_tasks_makers = list(filter(lambda user: count_open_tasks(user) <= max_count_tasks, possible_db_users))
    return child_tasks_makers
