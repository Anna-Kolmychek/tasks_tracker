from sqlalchemy import func, desc
from sqlalchemy.orm import Session, selectinload

from src.services.utils import (count_open_tasks,
                                get_free_user_by_position,
                                get_child_tasks_makers_by_max_count_tasks,
                                get_db_important_tasks
                                )
from src.tasks.schemas import TaskStatus
from src.users import models as models_user
from src.tasks import models as models_task
from src.constants import DIFF_COUNT_TASKS, LIMIT_SELECT as LIMIT


def get_busy_users(db: Session, skip: int = 0, limit: int = LIMIT):
    db_users = (db.query(models_user.User)
                .join(models_task.Task)
                .options(selectinload(models_user.User.tasks))
                .where(models_task.Task.status != TaskStatus.closed)
                .group_by(models_user.User.id)
                .order_by(desc(func.count(models_task.Task.id)))
                .offset(skip)
                .limit(limit)
                .all())
    return db_users


def get_important_tasks(db: Session):
    important_tasks = []

    # Получаем список важных задач
    db_tasks = get_db_important_tasks(db)

    # Получаем список всех сотрудников (чтобы минимизировать обращение к БД)
    db_all_users = (db.query(models_user.User)
                    .options(selectinload(models_user.User.tasks)))

    for task in db_tasks:
        # Получаем список наименее занятых сотрудников с должностью, указанной в важной задаче
        free_users = get_free_user_by_position(db_all_users=db_all_users, position_id=1, db=db)

        # Получаем список сотрудников, выполняющих дочерние задачи, для которых
        # количество назначенных на них задач не превышает установленной разницы
        # с количеством задач наименее занятых сотрудников
        possible_users = get_child_tasks_makers_by_max_count_tasks(
            db_all_users=db_all_users,
            max_count_tasks=count_open_tasks(free_users[0]) + DIFF_COUNT_TASKS,
            tasks=task.child_tasks
        )

        # В приоритете исполнители дочерних задач, но если их нет, выбираем наименее загруженных сотрудников
        if not possible_users: possible_users = free_users

        # Добавляем в список возможных исполнителей
        # сотрудника, на которого была назначена важная задача, если такой есть
        if task.maker_id and task.maker_id not in [user.id for user in possible_users]:
            possible_users.append(
                db_all_users.get(task.maker_id)
            )

        important_tasks.append(
            {
                'task': task,
                'deadline': task.deadline,
                'possible_makers': [f'{user.lastname} {user.firstname}' for user in possible_users]
            }
        )

    return important_tasks
