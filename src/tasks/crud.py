from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session
from src.tasks import schemas, models
from src.tasks.utils import check_relationship_fields


def create_task(task: schemas.TaskCreate, db: Session):
    check_relationship_fields(task=task, db=db)
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_all_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Task).offset(skip).limit(limit).all()


def get_task_by_id(id: int, db: Session):
    db_task = db.query(models.Task).get(id)
    if not db_task:
        raise HTTPException(status_code=404, detail=f'Task with id={id} not exist')
    return db_task


def update_task_by_id(id: int, task: schemas.TaskUpdate, db: Session, is_partial_update: bool):
    check_relationship_fields(task=task, db=db)
    db_task = get_task_by_id(id=id, db=db)
    if is_partial_update:
        task_data = task.model_dump(exclude_unset=True)
    else:
        task_data = task.model_dump()

    query = update(models.Task).where(models.Task.id == id).values(**task_data)
    db.execute(query)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task_by_id(db: Session, id: int):
    db_task = get_task_by_id(id=id, db=db)
    db.delete(db_task)
    db.commit()
    return db_task

