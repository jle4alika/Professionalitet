"""
Landlord database table
"""

import datetime
from sqlalchemy import func
from sqlalchemy import BigInteger, String
from sqlalchemy.dialects.sqlite import DATETIME
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.db import Base


class Landlord(Base):
    """
    Landlord table
    """

    __tablename__ = "landlords"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)

    created_time: Mapped[datetime.datetime] = mapped_column(
        DATETIME, default=func.now()
    )
