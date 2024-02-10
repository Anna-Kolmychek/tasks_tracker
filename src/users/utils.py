from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.users import models


def get_position_id(position: str, db: Session):
    db_position = db.query(models.Position).filter(models.Position.title == position).first()
    if db_position:
        return db_position.id
    return None


def check_duplicate_email(email: str, db: Session):
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(status_code=400, detail='Email already exist')


def check_duplicate_positions(title: str, db: Session):
    if db.query(models.Position).filter(models.Position.title == title).first():
        raise HTTPException(status_code=400, detail='Position already exist')
