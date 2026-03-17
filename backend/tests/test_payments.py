"""Тесты API платежей."""

import pytest
from httpx import AsyncClient

from backend.database.models import Payment, Order, User
from backend.database.models.payment import PaymentMethod, PaymentType


async def test_get_payments(client: AsyncClient, db_session):
    """Список платежей."""
    response = await client.get("/api/v1/payments")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


async def test_create_and_get_payment(
    client: AsyncClient, test_user: User, test_order: Order
):
    """Создание и получение платежа."""
    response = await client.post(
        "/api/v1/payments",
        json={
            "amount": 500.0,
            "currency": "RUB",
            "payment_method": "SBP",
            "payment_type": "rent",
            "order_id": test_order.id,
            "user_id": test_user.id,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 500.0
    assert data["payment_method"] == "SBP"
    assert data["order_id"] == test_order.id

    # Получить платёж
    get_response = await client.get(f"/api/v1/payments/{data['id']}")
    assert get_response.status_code == 200
    assert get_response.json()["id"] == data["id"]


async def test_check_payment(
    client: AsyncClient, test_user: User, test_order: Order, db_session
):
    """Проверка статуса платежа."""
    payment = Payment(
        amount=100.0,
        currency="RUB",
        payment_method=PaymentMethod.sbp,
        payment_type=PaymentType.rent,
        order_id=test_order.id,
        user_id=test_user.id,
        success=False,
    )
    db_session.add(payment)
    await db_session.commit()
    await db_session.refresh(payment)

    response = await client.get(f"/api/v1/payments/{payment.id}/check")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == payment.id
    assert data["success"] is False


async def test_update_payment_success(
    client: AsyncClient, test_user: User, test_order: Order, db_session
):
    """Обновление статуса платежа (подтверждение)."""
    payment = Payment(
        amount=200.0,
        currency="RUB",
        payment_method=PaymentMethod.card,
        payment_type=PaymentType.rent,
        order_id=test_order.id,
        user_id=test_user.id,
        success=False,
    )
    db_session.add(payment)
    await db_session.commit()
    await db_session.refresh(payment)

    response = await client.patch(
        f"/api/v1/payments/{payment.id}",
        json={"success": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


async def test_get_payment_not_found(client: AsyncClient):
    """Платёж не найден."""
    response = await client.get("/api/v1/payments/99999")
    assert response.status_code == 404
