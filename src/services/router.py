from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.services import services, schemas

router = APIRouter(
    prefix='/services',
    tags=['tasks services']
)


@router.get('/busy_users', response_model=list[schemas.UserWithTasks])
def get_busy_users(db: Session = Depends(get_db)):
    return services.get_busy_users(db=db)


@router.get('/important_tasks')
def get_important_tasks(db: Session = Depends(get_db)):
    return services.get_important_tasks(db=db)
