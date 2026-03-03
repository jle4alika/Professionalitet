from sqlalchemy import func, select, update, delete
from sqlalchemy.util import await_only

from database.models import User
from database.db import async_session


async def update_user_last_activity(tg_id: int):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(last_activity=func.now()))
        await session.commit()


async def get_user(tg_id: int) -> User | None:
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))


async def set_user_role(tg_id: int, role: str):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(role=role))
        await session.commit()


async def get_or_create_user(tg_id: int, username: str) -> User:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user: return user

        else:
            new_user = User(
                tg_id=tg_id,
                username=username
            )
            session.add(new_user)
            await session.commit()

            return await session.scalar(select(User).where(User.tg_id == tg_id))
