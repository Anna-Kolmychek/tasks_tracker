from typing import List

from sqlalchemy import String, MetaData
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

metadata_position = MetaData()


class Position(Base):
    __tablename__ = "job_position"

    # metadata = metadata_position

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)

    users: Mapped[List['User']] = relationship(back_populates='position')
    tasks: Mapped[List['Task']] = relationship(back_populates='maker_position')
