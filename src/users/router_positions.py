from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.users import schemas
from src.users import models
from src.users import crud_positions

router = APIRouter(
    prefix="/positions",
    tags=["positions CRUD"],
)


#
@router.post('/', response_model=schemas.Position)
async def create_position(position: schemas.PositionCreate, db: Session = Depends(get_db)):
    db_position = crud_positions.create_position(position=position, db=db)
    return db_position


@router.get('/', response_model=list[schemas.Position])
async def get_all_positions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_positions.get_all_positions(skip=skip, limit=limit, db=db)


@router.get('/{id}', response_model=schemas.Position)
async def get_position_by_id(id: int, db: Session = Depends(get_db)):
    return crud_positions.get_position_by_id(id=id, db=db)


@router.put('/{id}', response_model=schemas.Position)
async def update_position_by_id(id: int, position: schemas.PositionUpdate, db: Session = Depends(get_db)):
    return crud_positions.update_position_by_id(id=id, position=position, db=db)


@router.delete('/{id}', status_code=204)
async def delete_position_by_id(id: int, db: Session = Depends(get_db)):
    crud_positions.delete_position_by_id(id=id, db=db)
    return None
