"""
Base SQLAlchemy file
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config import settings

engine = create_async_engine(settings.SQLALCHEMY_URL)

async_session = async_sessionmaker(engine)


class Base(DeclarativeBase):
    """
    Base database model class
    """

    pass


async def async_main():
    """
    Creating tables
    :return:
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
