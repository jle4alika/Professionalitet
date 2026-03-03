"""
User database table
"""

import datetime
from sqlalchemy import func
from sqlalchemy import BigInteger, String
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import Mapped, mapped_column

from database.db import Base


class User(Base):
    """
    User table
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)

    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, default="", nullable=True)
    role: Mapped[str] = mapped_column(String, default="user", nullable=False)

    last_activity: Mapped[datetime.datetime] = mapped_column(
        DATETIME, default=func.now()
    )
    registration_time: Mapped[datetime.datetime] = mapped_column(
        DATETIME, default=func.now()
    )
