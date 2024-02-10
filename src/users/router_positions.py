from fastapi import APIRouter

from src.users.schemas import PositionCreate, Position

router = APIRouter(
    prefix="/positions",
    tags=["positions"],
)


@router.post('/')
async def create_position(position: PositionCreate):
    return {position}


@router.get('/')
async def get_all_positions():
    return {'get all positions'}


@router.get('/{id}')
async def get_position_by_id(id: int):
    return {f'get position with id {id}'}


@router.put('/{id}')
async def update_position_by_id(id: int, position: Position):
    return {f'update position with id {id}'}


@router.patch('/{id}')
async def update_position_by_id(id: int, position: Position):
    return {f'update position with id {id}'}


@router.delete('/{id}')
async def delete_position_by_id(id: int):
    return {f'delete position with id {id}'}
