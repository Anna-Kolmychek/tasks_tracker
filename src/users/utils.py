from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.users import models, schemas


def get_position_id(position: str, db: Session):
    db_position = db.query(models.Position).filter(models.Position.title == position).first()
    if db_position:
        return db_position.id
    return None

    #
def prepare_dict_user_data(user: schemas.User, db: Session):
    user_data = user.dict(exclude_unset=True)
    if user_data.get('position'):
        position_id = get_position_id(position=user.position, db=db)
        user_data.pop('position', None)
        user_data['position_id'] = position_id
    return user_data



def check_duplicate_email(email: str, db: Session):
    if db.query(models.User).filter(models.User.email == email).first():
        raise HTTPException(status_code=400, detail='Email already exist')


def check_duplicate_positions(title: str, db: Session):
    if db.query(models.Position).filter(models.Position.title == title).first():
        raise HTTPException(status_code=400, detail='Position already exist')
