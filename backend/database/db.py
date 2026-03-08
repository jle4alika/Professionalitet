"""
Base SQLAlchemy file
"""
import datetime

from sqlalchemy import DATETIME
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from project_config import settings
from typing import Annotated

engine = create_async_engine(settings.DATABASE_URL_asyncpg)

async_session = async_sessionmaker(
    engine,
    echo=True,
    # pool_size=5,
    # max_overflow=10,
)

idpk = Annotated[Mapped[int], mapped_column(primary_key=True)]

created_time = Annotated[datetime.datetime, mapped_column(
        DATETIME, server_default="TIMEZONE('utc', now())"
)]

updated_time = Annotated[datetime.datetime, mapped_column(
    DATETIME, server_default="TIMEZONE('utc', now())",
    onupdate=datetime.datetime.utcnow
)]

class Base(DeclarativeBase):
    """
    Base database model class
    """

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


async def async_main() -> None:
    """
    Creating tables
    :return:
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
