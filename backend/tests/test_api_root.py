"""Тесты корневого эндпоинта API."""

import pytest
from httpx import AsyncClient


async def test_root(client: AsyncClient):
    """Проверка корневого эндпоинта."""
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()

    assert "message" in data
    assert "docs" in data

    assert data["docs"] == "/docs"
    assert data["api_v1"] == "/api/v1"
