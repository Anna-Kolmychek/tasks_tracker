from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.constants import LIMIT_SELECT as LIMIT
from src.database import get_db
from src.tasks import schemas, crud

router = APIRouter(
    prefix='/tasks',
    tags=['tasks CRUD']
)


@router.post('/', response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(task=task, db=db)


@router.get('/', response_model=list[schemas.Task])
def get_all_tasks(skip: int = 0, limit: int = LIMIT, db: Session = Depends(get_db)):
    return crud.get_all_tasks(skip=skip, limit=limit, db=db)


@router.get('/{id}', response_model=schemas.Task)
def get_task_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_task_by_id(id=id, db=db)


@router.put('/{id}', response_model=schemas.Task)
def update_task_by_id(id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    return crud.update_task_by_id(id=id, task=task, db=db, is_partial_update=False)


@router.patch('/{id}', response_model=schemas.Task)
def update_task_by_id(id: int, task: schemas.TaskPartialUpdate, db: Session = Depends(get_db)):
    return crud.update_task_by_id(id=id, task=task, db=db, is_partial_update=True)


@router.delete('/{id}', response_model=schemas.Task)
def delete_task_by_id(id: int, db: Session = Depends(get_db)):
    return crud.delete_task_by_id(id=id, db=db)
