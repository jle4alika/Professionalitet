"""Тесты API пользователей."""

import pytest
from httpx import AsyncClient

from backend.database.models import User


async def test_registration(client: AsyncClient):
    """Регистрация нового пользователя."""
    response = await client.post(
        "/api/v1/users/registration",
        json={
            "username": "newuser",
            "password": "password123",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user_id"] is not None


async def test_registration_duplicate_username(client: AsyncClient, test_user: User):
    """Регистрация с существующим username."""
    response = await client.post(
        "/api/v1/users/registration",
        json={
            "username": test_user.username,
            "password": "password123",
            "email": "other@example.com",
        },
    )
    assert response.status_code == 400


async def test_login(client: AsyncClient, test_user: User):
    """Авторизация пользователя."""
    response = await client.post(
        "/api/v1/users/login",
        json={"username": test_user.username, "password": "testpass123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user_id"] == test_user.id


async def test_login_wrong_password(client: AsyncClient, test_user: User):
    """Авторизация с неверным паролем."""
    response = await client.post(
        "/api/v1/users/login",
        json={"username": test_user.username, "password": "wrongpassword"},
    )
    assert response.status_code == 401


async def test_logout(client: AsyncClient, auth_client: AsyncClient):
    """Выход из системы."""
    response = await auth_client.post("/api/v1/users/logout")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "message" in data


async def test_get_users(client: AsyncClient, test_user: User):
    """Список пользователей."""
    response = await client.get("/api/v1/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    usernames = [u["username"] for u in data]
    assert test_user.username in usernames


async def test_get_user(client: AsyncClient, test_user: User):
    """Получить пользователя по ID."""
    response = await client.get(f"/api/v1/users/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["username"] == test_user.username
    assert data["email"] == test_user.email


async def test_get_user_not_found(client: AsyncClient):
    """Пользователь не найден."""
    response = await client.get("/api/v1/users/99999")
    assert response.status_code == 404


async def test_update_user(client: AsyncClient, test_user: User):
    """Обновление пользователя."""
    response = await client.patch(
        f"/api/v1/users/{test_user.id}",
        json={"first_name": "Updated", "last_name": "Name"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Updated"
    assert data["last_name"] == "Name"


async def test_delete_user(client: AsyncClient, test_user: User):
    """Удаление пользователя."""
    response = await client.delete(f"/api/v1/users/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "message" in data

    # Проверяем что пользователь удалён
    get_response = await client.get(f"/api/v1/users/{test_user.id}")
    assert get_response.status_code == 404
