from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.positions import models


def check_duplicate_positions(title: str, db: Session):
    if db.query(models.Position).filter(models.Position.title == title).first():
        raise HTTPException(status_code=400, detail='Position already exist')
