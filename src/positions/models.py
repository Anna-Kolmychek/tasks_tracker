from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Position(Base):
    __tablename__ = "job_position"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)

    users: Mapped[List['User']] = relationship(back_populates='position')
    tasks: Mapped[List['Task']] = relationship(back_populates='maker_position')
