"""Тесты API заказов."""

import pytest
from httpx import AsyncClient

from backend.database.models import Order, User, VendingMachine


async def test_get_orders(client: AsyncClient, test_order: Order):
    """Список заказов."""
    response = await client.get("/api/v1/orders")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    ids = [o["id"] for o in data]
    assert test_order.id in ids


async def test_get_orders_filter_by_user(
    client: AsyncClient, test_order: Order, test_user: User
):
    """Список заказов с фильтром по user_id."""
    response = await client.get(f"/api/v1/orders?user_id={test_user.id}")
    assert response.status_code == 200

    data = response.json()
    assert all(o["user_id"] == test_user.id for o in data)


async def test_get_order(client: AsyncClient, test_order: Order):
    """Получить заказ по ID."""
    response = await client.get(f"/api/v1/orders/{test_order.id}")
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == test_order.id
    assert data["duration"] == test_order.duration
    assert data["user_id"] == test_order.user_id


async def test_get_order_not_found(client: AsyncClient):
    """Заказ не найден."""
    response = await client.get("/api/v1/orders/99999")
    assert response.status_code == 404


async def test_create_order(client: AsyncClient, test_user: User, db_session):
    """Создание заказа."""
    vm = VendingMachine(title="Free Machine", amount_in_hour=50.0, rented=False)
    db_session.add(vm)

    await db_session.commit()
    await db_session.refresh(vm)

    response = await client.post(
        "/api/v1/orders",
        json={
            "duration": 12,
            "vending_machine_id": vm.id,
            "user_id": test_user.id,
        },
    )
    assert response.status_code == 201
    data = response.json()

    assert data["duration"] == 12
    assert data["vending_machine_id"] == vm.id
    assert data["user_id"] == test_user.id
    assert "id" in data


async def test_create_order_vm_not_found(client: AsyncClient, test_user: User):
    """Создание заказа — аппарат не найден."""
    response = await client.post(
        "/api/v1/orders",
        json={
            "duration": 12,
            "vending_machine_id": 99999,
            "user_id": test_user.id,
        },
    )
    assert response.status_code == 404


async def test_create_order_vm_already_rented(
    client: AsyncClient, test_user: User, test_order: Order
):
    """Создание заказа — аппарат уже арендован (используется в test_order)."""
    response = await client.post(
        "/api/v1/orders",
        json={
            "duration": 12,
            "vending_machine_id": test_order.vending_machine_id,
            "user_id": test_user.id,
        },
    )
    assert response.status_code == 400


async def test_update_order(client: AsyncClient, test_order: Order):
    """Обновление заказа (отметка истечения)."""
    response = await client.patch(
        f"/api/v1/orders/{test_order.id}",
        json={"expired": True},
    )
    assert response.status_code == 200
    data = response.json()

    assert data["expired"] is True


async def test_delete_order(client: AsyncClient, test_order: Order):
    """Удаление заказа."""
    order_id = test_order.id
    response = await client.delete(f"/api/v1/orders/{order_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True

    get_response = await client.get(f"/api/v1/orders/{order_id}")
    assert get_response.status_code == 404
