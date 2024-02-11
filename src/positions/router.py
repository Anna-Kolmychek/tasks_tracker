from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src.positions import schemas
from src.positions import crud

router = APIRouter(
    prefix="/positions",
    tags=["positions CRUD"],
)


#
@router.post('/', response_model=schemas.Position)
async def create_position(position: schemas.PositionCreate, db: Session = Depends(get_db)):
    return crud.create_position(position=position, db=db)


@router.get('/', response_model=list[schemas.Position])
async def get_all_positions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_all_positions(skip=skip, limit=limit, db=db)


@router.get('/{id}', response_model=schemas.Position)
async def get_position_by_id(id: int, db: Session = Depends(get_db)):
    return crud.get_position_by_id(id=id, db=db)


@router.put('/{id}', response_model=schemas.Position)
async def update_position_by_id(id: int, position: schemas.PositionUpdate, db: Session = Depends(get_db)):
    return crud.update_position_by_id(id=id, position=position, db=db, is_partial_update=False)


@router.patch('/{id}', response_model=schemas.Position)
async def partial_update_position_by_id(id: int, position: schemas.PositionPartialUpdate,
                                        db: Session = Depends(get_db)):
    return crud.update_position_by_id(id=id, position=position, db=db, is_partial_update=True)


@router.delete('/{id}', response_model=schemas.Position)
async def delete_position_by_id(id: int, db: Session = Depends(get_db)):
    return crud.delete_position_by_id(id=id, db=db)
