"""
User database table
"""

import datetime
import enum
from typing import Optional

from sqlalchemy import func, Float
from sqlalchemy import BigInteger, String
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.db import Base, idpk, created_time, updated_time

class UserStatus(enum.Enum):
    tenant = "tenant"
    landlord = "landlord"

class User(Base):
    """
    User table (Пользователь)
    """

    __tablename__ = "users"

    id: Mapped[idpk]

    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str]
    phone_number: Mapped[Optional[str]]
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]

    balance: Mapped[float] = mapped_column(Float, default=0)
    status: Mapped[UserStatus] = mapped_column(default="tenant")

    orders: Mapped[list["Order"]] = relationship(
        back_populates="user",
        order_by="Order.expired.desc()",
    )

    payments: Mapped[list["Payment"]] = relationship(
        back_populates="user",
    )

    created_time: Mapped[created_time]
    updated_time: Mapped[updated_time]
