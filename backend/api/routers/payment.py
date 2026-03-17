"""
REST API для платежей
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select

from backend.api.schemas.payment import PaymentsDTO, PaymentsAddDTO, PaymentsUpdateDTO
from backend.api.schemas.common import PaymentCheckResponse
from backend.database.models import Payment
from backend.api.dependencies.db_session import db_session

router = APIRouter(
    tags=["Система оплат"],
    prefix="/payments",
)


@router.get("/", response_model=list[PaymentsDTO])
async def get_payments(
    session: db_session,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    user_id: int | None = None,
    order_id: int | None = None,
    success: bool | None = None,
) -> list[PaymentsDTO]:
    """Список платежей с пагинацией и фильтрами."""
    query = select(Payment).offset(skip).limit(limit)

    if user_id is not None:
        query = query.where(Payment.user_id == user_id)
    if order_id is not None:
        query = query.where(Payment.order_id == order_id)
    if success is not None:
        query = query.where(Payment.success == success)

    result = await session.execute(query)
    payments = result.scalars().all()

    return [PaymentsDTO.model_validate(p) for p in payments]


@router.get("/{payment_id}", response_model=PaymentsDTO)
async def get_payment(payment_id: int, session: db_session) -> PaymentsDTO:
    """Получить платёж по ID."""
    query = select(Payment).where(Payment.id == payment_id)
    result = await session.execute(query)
    payment = result.scalar_one_or_none()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    return PaymentsDTO.model_validate(payment)


@router.get("/{payment_id}/check", response_model=PaymentCheckResponse)
async def check_payment(payment_id: int, session: db_session) -> PaymentCheckResponse:
    """Проверить статус платежа."""
    query = select(Payment).where(Payment.id == payment_id)
    result = await session.execute(query)
    payment = result.scalar_one_or_none()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    return PaymentCheckResponse(id=payment.id, success=payment.success)


@router.post("/", response_model=PaymentsDTO, status_code=201)
async def create_payment(data: PaymentsAddDTO, session: db_session) -> PaymentsDTO:
    """Создать новый платёж."""
    payment = Payment(
        amount=data.amount,
        currency=data.currency or "RUB",
        payment_method=data.payment_method,
        payment_type=data.payment_type,
        order_id=data.order_id,
        user_id=data.user_id,
    )
    session.add(payment)
    await session.commit()
    await session.refresh(payment)

    # В реальной системе здесь был бы вызов платёжного провайдера
    return PaymentsDTO.model_validate(payment)


@router.patch("/{payment_id}", response_model=PaymentsDTO)
async def update_payment(
    payment_id: int, data: PaymentsUpdateDTO, session: db_session
) -> PaymentsDTO:
    """Обновить статус платежа (подтверждение оплаты)."""
    query = select(Payment).where(Payment.id == payment_id)
    result = await session.execute(query)
    payment = result.scalar_one_or_none()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(payment, key, value)

    await session.commit()
    await session.refresh(payment)

    return PaymentsDTO.model_validate(payment)
