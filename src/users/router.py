from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.constants import LIMIT_SELECT as LIMIT
from src.database import get_db
from src.users import schemas
from src.users import crud

router = APIRouter(
    prefix="/users",
    tags=["users CRUD"],
)


@router.post('/', response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(user=user, db=db)


@router.get('/', response_model=list[schemas.User])
async def get_all_users(skip: int = 0, limit: int = LIMIT, db: Session = Depends(get_db)):
    return crud.get_all_users(db=db, skip=skip, limit=limit)


@router.get('/{id}', response_model=schemas.User)
async def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_user_by_id(id=id, db=db)


@router.put('/{id}', response_model=schemas.User)
async def update_user_by_id(id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user_by_id(id=id, user=user, db=db, is_partial_update=False)


@router.patch('/{id}', response_model=schemas.User)
async def partial_update_user_by_id(id: int, user: schemas.UserPartialUpdate, db: Session = Depends(get_db)):
    return crud.update_user_by_id(id=id, user=user, db=db, is_partial_update=True)


@router.delete('/{id}')
async def delete_user_by_id(id: int, db: Session = Depends(get_db)):
    return crud.delete_user_by_id(id=id, db=db)
