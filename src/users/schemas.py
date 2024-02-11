from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    position: str | None = None


class UserUpdate(UserCreate):
    pass


class UserPartialUpdate(UserUpdate):
    email: str | None = None
    password: str | None = None
    position: str | None = None


class User(UserBase):
    id: int
    position_id: int | None
