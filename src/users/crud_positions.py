from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.users import schemas
from src.users import models
from src.users.utils import check_duplicate_positions


def create_position(position: schemas.PositionCreate, db: Session):
    check_duplicate_positions(title=position.title, db=db)

    db_position = models.Position(
        title=position.title,
    )
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position


def get_all_positions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Position).offset(skip).limit(limit).all()


def get_position_by_id(id: int, db: Session):
    db_position = db.query(models.Position).get(id)
    if not db_position:
        raise HTTPException(status_code=404, detail=f'Position with id={id} not exist')
    return db_position


def update_position_by_id(db: Session, position: schemas.PositionUpdate, id: int):
    db_position = get_position_by_id(id=id, db=db)
    if db_position.title != position.title:
        check_duplicate_positions(title=position.title, db=db)
    db_position.title = position.title

    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position


def delete_position_by_id(db: Session, id: int):
    db_position = get_position_by_id(id=id, db=db)
    db.delete(db_position)
    db.commit()
    return db_position
