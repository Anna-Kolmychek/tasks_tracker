from typing import Optional, List

from sqlalchemy import String, ForeignKey, MetaData
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

metadata_user = MetaData()

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String)
    firstname: Mapped[Optional[str]] = mapped_column(String, default=None)
    lastname: Mapped[Optional[str]] = mapped_column(String, default=None)
    password: Mapped[str] = mapped_column(String)
    position_id: Mapped[Optional[int]] = mapped_column(ForeignKey('job_position.id'), default=None)

    position: Mapped['Position'] = relationship(back_populates='users')
    tasks: Mapped[List['Task']] = relationship(back_populates='maker')
