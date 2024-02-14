from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.services import services, schemas
from src.constants import LIMIT_SELECT as LIMIT

router = APIRouter(
    prefix='/services',
    tags=['tasks services']
)


@router.get('/busy_users', response_model=list[schemas.UserWithTasks])
def get_busy_users(db: Session = Depends(get_db), skip: int = 0, limit: int = LIMIT):
    return services.get_busy_users(db=db, skip=skip, limit=limit)


@router.get('/important_tasks', response_model=list[schemas.ImportantTasks])
def get_important_tasks(db: Session = Depends(get_db)):
    return services.get_important_tasks(db=db)
