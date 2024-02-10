from typing import Annotated, Optional
from pydantic import BaseModel

# def convert_to_optional(schema):
#     return {k: Optional[v] for k, v in schema.__annotations__.items()}

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    position: str | None = None


class UserUpdate(UserCreate):
    pass

# class UserOptionalUpdate(UserUpdate):
#     __annotations__ = convert_to_optional(UserUpdate)


class User(UserBase):
    id: int
    position_id: int | None

    class Config:
        orm_mode = True


class PositionBase(BaseModel):
    title: str


class PositionCreate(PositionBase):
    pass


class PositionUpdate(PositionBase):
    pass

# class PositionOptionalUpdate(PositionUpdate):
#     __annotations__ = convert_to_optional(PositionUpdate)

class Position(PositionBase):
    id: int

    class Config:
        orm_mode = True
