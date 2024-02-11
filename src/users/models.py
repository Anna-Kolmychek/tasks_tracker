from typing import Optional, List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
# from src.tasks.models import Task


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    position_id: Mapped[Optional[int]] = mapped_column(ForeignKey('job_position.id'))

    position: Mapped['Position'] = relationship(back_populates='users')
    # tasks: Mapped[List['Task']] = relationship(back_populates='maker')


class Position(Base):
    __tablename__ = "job_position"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)

    # users: Mapped[List['User']] = relationship(back_populates='position')
    # tasks: Mapped[List['Task']] = relationship(back_populates='maker_position')
