"""
REST API для пользователей
"""

from fastapi import APIRouter, Response, Depends, HTTPException, Query
from backend.api.schemas.user import (
    UsersDTO,
    UsersAddDTO,
    UsersUpdateDTO,
    UsersLoginDTO,
)
from backend.api.schemas.common import (
    LoginResponse,
    AuthCheckResponse,
    MessageResponse,
)
from backend.database.models import User
from backend.database.models.user import UserStatus
from project_config import security, config
from backend.api.dependencies.db_session import db_session
from sqlalchemy import select, and_

router = APIRouter(
    tags=["Пользователи"],
    prefix="/users",
)


@router.post("/login", response_model=LoginResponse)
async def login(
    creds: UsersLoginDTO, response: Response, session: db_session
) -> LoginResponse:
    """Авторизация пользователя."""
    query = select(User).where(
        User.username == creds.username, User.password == creds.password
    )
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if user:
        access_token = security.create_access_token(uid=str(user.id))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, access_token)
        return LoginResponse(access_token=access_token, user_id=user.id)

    raise HTTPException(status_code=401, detail="Incorrect username or password")


@router.post("/logout", response_model=MessageResponse)
async def logout(response: Response) -> MessageResponse:
    """Выход из системы — удаление токена из cookies."""
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return MessageResponse(message="Успешный выход из системы")


@router.get(
    "/auth",
    response_model=AuthCheckResponse,
    dependencies=[Depends(security.access_token_required)],
)
async def protected() -> AuthCheckResponse:
    """Проверка авторизации."""
    return AuthCheckResponse(auth=True)


@router.post("/registration", response_model=LoginResponse)
async def registration(
    creds: UsersAddDTO, response: Response, session: db_session
) -> LoginResponse:
    """Регистрация нового пользователя."""
    query = select(User).where(User.username == creds.username)
    result = await session.execute(query)

    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already exists")

    query_email = select(User).where(User.email == creds.email)
    result_email = await session.execute(query_email)
    if result_email.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already exists")

    try:
        new_user = User(**creds.model_dump(exclude_none=True))
        session.add(new_user)

        await session.commit()
        await session.refresh(new_user)
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    access_token = security.create_access_token(uid=str(new_user.id))
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, access_token)

    return LoginResponse(access_token=access_token, user_id=new_user.id)


@router.get("/", response_model=list[UsersDTO])
async def get_users(
    session: db_session,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> list[UsersDTO]:
    """Список пользователей с пагинацией."""
    query = select(User).offset(skip).limit(limit)
    result = await session.execute(query)
    users = result.scalars().all()

    return [UsersDTO.model_validate(u) for u in users]


@router.get("/{user_id}", response_model=UsersDTO)
async def get_user(user_id: int, session: db_session) -> UsersDTO:
    """Получить пользователя по ID."""
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UsersDTO.model_validate(user)


@router.patch("/{user_id}", response_model=UsersDTO)
async def update_user(
    user_id: int, data: UsersUpdateDTO, session: db_session
) -> UsersDTO:
    """Обновить пользователя."""
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = data.model_dump(exclude_unset=True)

    # Проверка уникальности username/email при обновлении
    if "username" in update_data:
        exists = await session.execute(
            select(User).where(
                and_(User.username == update_data["username"], User.id != user_id)
            )
        )
        if exists.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username already exists")

    if "email" in update_data:
        exists = await session.execute(
            select(User).where(
                and_(User.email == update_data["email"], User.id != user_id)
            )
        )
        if exists.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already exists")

    for key, value in update_data.items():
        if key == "status" and value is not None:
            try:
                setattr(user, key, UserStatus(value))
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid status value")
        elif key != "status":
            setattr(user, key, value)

    await session.commit()
    await session.refresh(user)

    return UsersDTO.model_validate(user)


@router.delete("/{user_id}", response_model=MessageResponse)
async def delete_user(user_id: int, session: db_session) -> MessageResponse:
    """Удалить пользователя."""
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()

    return MessageResponse(message="Пользователь успешно удалён")
