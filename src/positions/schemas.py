from pydantic import BaseModel


class PositionBase(BaseModel):
    title: str


class PositionCreate(PositionBase):
    pass


class PositionUpdate(PositionBase):
    pass


class PositionPartialUpdate(PositionUpdate):
    pass


class Position(PositionBase):
    id: int
