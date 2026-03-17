"""Тесты API вендинговых аппаратов."""

import pytest
from httpx import AsyncClient

from backend.database.models import VendingMachine


async def test_get_vending_machines(
    client: AsyncClient, test_vending_machine: VendingMachine
):
    """Список вендинговых аппаратов."""
    response = await client.get("/api/v1/vending-machines")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(m["id"] == test_vending_machine.id for m in data)


async def test_get_vending_machine(
    client: AsyncClient, test_vending_machine: VendingMachine
):
    """Получить аппарат по ID."""
    response = await client.get(f"/api/v1/vending-machines/{test_vending_machine.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_vending_machine.id
    assert data["title"] == test_vending_machine.title
    assert data["amount_in_hour"] == test_vending_machine.amount_in_hour


async def test_get_vending_machine_not_found(client: AsyncClient):
    """Аппарат не найден."""
    response = await client.get("/api/v1/vending-machines/99999")
    assert response.status_code == 404


async def test_create_vending_machine(client: AsyncClient):
    """Создание аппарата."""
    response = await client.post(
        "/api/v1/vending-machines",
        json={"title": "New Machine", "amount_in_hour": 150.0},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Machine"
    assert data["amount_in_hour"] == 150.0
    assert data["rented"] is False
    assert "id" in data


async def test_update_vending_machine(
    client: AsyncClient, test_vending_machine: VendingMachine
):
    """Обновление аппарата."""
    response = await client.patch(
        f"/api/v1/vending-machines/{test_vending_machine.id}",
        json={"title": "Updated Title", "amount_in_hour": 200.0},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["amount_in_hour"] == 200.0


async def test_delete_vending_machine(client: AsyncClient, db_session):
    """Удаление аппарата."""
    vm = VendingMachine(title="To Delete", amount_in_hour=10.0, rented=False)
    db_session.add(vm)
    await db_session.commit()
    await db_session.refresh(vm)
    vm_id = vm.id

    response = await client.delete(f"/api/v1/vending-machines/{vm_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True

    get_response = await client.get(f"/api/v1/vending-machines/{vm_id}")
    assert get_response.status_code == 404
