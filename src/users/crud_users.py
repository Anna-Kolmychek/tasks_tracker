from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import update
from sqlalchemy.orm import Session
from src.users import schemas
from src.users import models
from src.users.utils import get_position_id, check_duplicate_email, prepare_dict_user_data


def create_user(user: schemas.UserCreate, db: Session):
    check_duplicate_email(email=user.email, db=db)

    user_data = prepare_dict_user_data(user, db=db)
    db_user = models.User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_id(id: int, db: Session):
    db_user = db.query(models.User).get(id)
    if not db_user:
        raise HTTPException(status_code=404, detail=f'User with id={id} not exist')
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def update_user_by_id(db: Session, user: schemas.UserUpdate, id: int):
    db_user = get_user_by_id(id=id, db=db)
    if db_user.email != user.email:
        check_duplicate_email(email=user.email, db=db)

    user_data = prepare_dict_user_data(user, db=db)

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
