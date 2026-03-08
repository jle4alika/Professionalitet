"""
VendingMachine database table
"""

import datetime
from sqlalchemy import func, Float
from sqlalchemy import BigInteger, String
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.db import Base, idpk, created_time, updated_time

class VendingMachine(Base):
    """
    VendingMachine table
    """

    __tablename__ = "vending_machines"

    id: Mapped[idpk]

    title: Mapped[str]
    amount_in_hour: Mapped[float]

    rented: Mapped[bool] = mapped_column(default=False)

    orders: Mapped[list["Order"]] = relationship(
        back_populates="vending_machine",
        order_by="Order.expired.desc()",
        lazy='selectin'
    )

    created_time: Mapped[created_time]
    updated_time: Mapped[updated_time]
