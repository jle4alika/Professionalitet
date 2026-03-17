"""
Landlord database table
"""

import datetime
import enum

from sqlalchemy import func, ForeignKey, Float
from sqlalchemy import BigInteger, String
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.db import Base, idpk, created_time, updated_time


class PaymentMethod(enum.Enum):
    sbp = "SBP"
    card = "CARD"


class PaymentType(enum.Enum):
    rent = "rent"
    extension = "extension"


class Payment(Base):
    """
    Payment table (Оплата)
    """

    __tablename__ = "payments"

    id: Mapped[idpk]

    amount: Mapped[float]
    currency: Mapped[str] = mapped_column(String, default="RUB")
    payment_method: Mapped[PaymentMethod]
    payment_type: Mapped[PaymentType] = mapped_column(default=PaymentType.rent)
    success: Mapped[bool] = mapped_column(default=False)

    created_time: Mapped[created_time]
    updated_time: Mapped[updated_time]

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    order: Mapped["Order"] = relationship(
        back_populates="payment",
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(
        back_populates="payments",
    )
