"""
Landlord database table
"""

import datetime
from sqlalchemy import func, ForeignKey
from sqlalchemy import BigInteger, String
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.db import Base, idpk, created_time, updated_time


class Order(Base):
    """
    Landlord table (Арендодатель)
    """

    __tablename__ = "orders"

    id: Mapped[idpk]

    duration: Mapped[int]
    end_date: Mapped[datetime.datetime]
    expired: Mapped[bool] = mapped_column(default=False)

    created_time: Mapped[created_time]
    updated_time: Mapped[updated_time]

    vending_machine_id: Mapped[int] = mapped_column(
        ForeignKey("vending_machines.id", ondelete="CASCADE")
    )
    vending_machine: Mapped["VendingMachine"] = relationship(
        back_populates="orders",
    )

    payment: Mapped[list["Payment"]] = relationship(
        back_populates="order", order_by="Payment.success.desc()", lazy="joined"
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(
        back_populates="orders",
    )
