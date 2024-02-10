from typing import Annotated
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    position: str | None = None


class UserUpdate(UserCreate):
    pass


class User(UserBase):
    id: int
    position_id: int | None

    class Config:
        orm_mode = True


class PositionBase(BaseModel):
    title: str


class PositionCreate(PositionBase):
    pass


class Position(PositionBase):
    id: int

    class Config:
        orm_mode = True
