from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.users import schemas as schemas_users, models as models_users
from src.positions import models as models_positions


def get_position_id(position: str, db: Session):
    db_position = db.query(models_positions.Position).filter(models_positions.Position.title == position).first()
    if db_position:
        return db_position.id
    return None


def convert_position_in_position_id(user_data: dict, db: Session):
    if 'position' in user_data:
        position_id = get_position_id(position=user_data.get('position'), db=db)
        user_data.pop('position', None)
        user_data['position_id'] = position_id
    return user_data


def check_duplicate_email(email: str, db: Session):
    if db.query(models_users.User).filter(models_users.User.email == email).first():
        raise HTTPException(status_code=400, detail='Email already exist')
