from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.tasks import schemas
from src.tasks import models
from src.users import models as models_users
from src.positions import models as models_positions


def check_relationship_fields(task: schemas.TaskCreate, db: Session):
    if task.parent_task_id is not None:
        if not db.get(models.Task, task.parent_task_id):
            raise HTTPException(status_code=400, detail=f'Task with id={task.parent_task_id} not exist')
    if task.maker_id is not None:
        if not db.get(models_users.User, task.maker_id):
            raise HTTPException(status_code=400, detail=f'User with id={task.maker_id} not exist')
    if task.maker_position_id is not None:
        if not db.get(models_positions.Position, task.maker_position_id):
            raise HTTPException(status_code=400, detail=f'User with id={task.maker_position_id} not exist')
