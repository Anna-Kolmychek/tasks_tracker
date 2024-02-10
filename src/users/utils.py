from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.users import models


def get_position_id(position: str):
    return None


def check_duplicate_email(email: str, db: Session):
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(status_code=400, detail='Email already exist')
