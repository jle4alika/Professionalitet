"""Тесты API аренды."""

import pytest
from httpx import AsyncClient

from backend.database.models import Order, VendingMachine, User


async def test_get_active_rents(client: AsyncClient, test_order: Order):
    """Список активных аренд."""
    response = await client.get("/api/v1/rents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(o["id"] == test_order.id and not o["expired"] for o in data)


async def test_get_available_machines(
    client: AsyncClient, db_session, test_order: Order
):
    """Список доступных для аренды аппаратов (не арендованных)."""
    response = await client.get("/api/v1/rents/available")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # test_order арендует аппарат, поэтому он не должен быть в available
    vm_id = test_order.vending_machine_id
    assert not any(m["id"] == vm_id for m in data)


async def test_create_rent(client: AsyncClient, test_user: User, db_session):
    """Создание аренды."""
    vm = VendingMachine(title="Available VM", amount_in_hour=75.0, rented=False)
    db_session.add(vm)
    await db_session.commit()
    await db_session.refresh(vm)

    response = await client.post(
        "/api/v1/rents",
        json={
            "duration": 48,
            "vending_machine_id": vm.id,
            "user_id": test_user.id,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["duration"] == 48
    assert data["vending_machine_id"] == vm.id
    assert data["user_id"] == test_user.id
