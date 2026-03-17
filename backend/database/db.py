"""
Base SQLAlchemy file
"""

import datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column
from project_config import settings
from typing import Annotated

engine = create_async_engine(settings.DATABASE_URL_asyncpg)

async_session = async_sessionmaker(
    engine,
    echo=True,
    # pool_size=5,
    # max_overflow=10,
)


async def get_session():
    async with async_session() as session:
        yield session


idpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

created_time = Annotated[
    datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]

updated_time = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.datetime.utcnow
    ),
]


class Base(DeclarativeBase):
    """
    Base database model class
    """

    repr_cols: set = set()
    repr_cols_num: int = 3

    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        repr_cols = getattr(self.__class__, "repr_cols", set())
        repr_cols_num = getattr(self.__class__, "repr_cols_num", 3)
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in repr_cols or idx < repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


async def async_main() -> None:
    """
    Creating tables
    :return:
    """
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
