from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    firstname: str | None = None
    lastname: str | None = None
    position: str | None = None


class UserUpdate(UserCreate):
    pass


class UserPartialUpdate(UserUpdate):
    email: str | None = None
    firstname: str | None = None
    lastname: str | None = None
    password: str | None = None
    position: str | None = None


class User(UserBase):
    id: int
    position_id: int | None
