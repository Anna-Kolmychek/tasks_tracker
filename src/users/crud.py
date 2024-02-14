from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session

from src.constants import LIMIT_SELECT as LIMIT
from src.users import schemas
from src.users import models
from src.users.utils import check_duplicate_email, convert_position_in_position_id


def create_user(user: schemas.UserCreate, db: Session):
    check_duplicate_email(email=user.email, db=db)

    user_data = convert_position_in_position_id(user.model_dump(), db=db)
    db_user = models.User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_users(db: Session, skip: int = 0, limit: int = LIMIT):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_id(id: int, db: Session):
    db_user = db.query(models.User).get(id)
    if not db_user:
        raise HTTPException(status_code=404, detail=f'User with id={id} not exist')
    return db_user


def update_user_by_id(db: Session, user: schemas.UserUpdate, id: int, is_partial_update: bool):
    db_user = get_user_by_id(id=id, db=db)
    if db_user.email != user.email:
        check_duplicate_email(email=user.email, db=db)

    if is_partial_update:
        user_data = user.model_dump(exclude_unset=True)
    else:
        user_data = user.model_dump()
    user_data = convert_position_in_position_id(user_data, db=db)

    query = update(models.User).where(models.User.id == id).values(**user_data)
    db.execute(query)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user_by_id(db: Session, id: int):
    db_user = get_user_by_id(id=id, db=db)
    db.delete(db_user)
    db.commit()
    return db_user
