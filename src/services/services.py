from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload, joinedload

from src.services.utils import (count_open_tasks,
                                filter_by_child_in_work,
                                get_free_user_by_position,
                                get_child_tasks_makers_by_max_count_tasks,
                                )
from src.tasks.schemas import TaskStatus
from src.users import models as models_user
from src.tasks import models as models_task
from src.constants import DIFF_COUNT_TASKS, LIMIT_SELECT as LIMIT


def get_busy_users(db: Session):
    db_users = db.query(models_user.User).options(selectinload(models_user.User.tasks)).all()
    db_users.sort(key=count_open_tasks, reverse=True)
    return db_users


def get_important_tasks(db: Session):
    important_tasks = []

    db_tasks = (db.query(models_task.Task)
                .options(selectinload(models_task.Task.child_tasks))
                .where(models_task.Task.status == TaskStatus.new)
                .all())
    db_tasks = filter_by_child_in_work(db_tasks)

    db_all_users = (db.query(models_user.User)
                    .options(selectinload(models_user.User.tasks)))

    for task in db_tasks:
        free_users = get_free_user_by_position(db_all_users=db_all_users, position_id=1, db=db)

        posible_users = get_child_tasks_makers_by_max_count_tasks(
            db_all_users=db_all_users,
            max_count_tasks=count_open_tasks(free_users[0]) + DIFF_COUNT_TASKS,
            tasks=task.child_tasks
        )

        if not posible_users: posible_users = free_users
        if task.maker_id and task.maker_id not in [user.id for user in posible_users]:
            posible_users.append(
                db_all_users.get(task.maker_id)
            )

        important_tasks.append(
            {
                'task': task,
                'deadline': task.deadline,
                'posible_makers': posible_users
            }
        )

    return important_tasks
