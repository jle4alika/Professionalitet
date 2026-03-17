"""
REST API для аренды — высокоуровневые эндпоинты
"""

import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select

from backend.api.schemas.order import OrdersDTO, OrdersAddDTO
from backend.api.schemas.common import AvailableMachineItem
from backend.database.models import Order, VendingMachine
from backend.api.dependencies.db_session import db_session

router = APIRouter(
    tags=["Аренда"],
    prefix="/rents",
)


@router.get("/", response_model=list[OrdersDTO])
async def get_active_rents(
    session: db_session,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    user_id: int | None = None,
) -> list[OrdersDTO]:
    """Список активных аренд (не истёкших заказов)."""
    query = select(Order).where(Order.expired == False).offset(skip).limit(limit)

    if user_id is not None:
        query = query.where(Order.user_id == user_id)

    result = await session.execute(query)
    orders = result.unique().scalars().all()

    return [OrdersDTO.model_validate(o) for o in orders]


@router.get("/available", response_model=list[AvailableMachineItem])
async def get_available_machines(
    session: db_session,
) -> list[AvailableMachineItem]:
    """Список вендинговых аппаратов, доступных для аренды."""
    query = select(VendingMachine).where(VendingMachine.rented == False)
    result = await session.execute(query)
    machines = result.scalars().all()

    return [
        AvailableMachineItem(id=m.id, title=m.title, amount_in_hour=m.amount_in_hour)
        for m in machines
    ]


@router.post("/", response_model=OrdersDTO, status_code=201)
async def create_rent(data: OrdersAddDTO, session: db_session) -> OrdersDTO:
    """Создать новую аренду (заказ)."""
    vm_query = select(VendingMachine).where(
        VendingMachine.id == data.vending_machine_id
    )
    vm_result = await session.execute(vm_query)
    vending_machine = vm_result.scalar_one_or_none()

    if not vending_machine:
        raise HTTPException(status_code=404, detail="Vending machine not found")
    if vending_machine.rented:
        raise HTTPException(status_code=400, detail="Vending machine is already rented")

    end_date = datetime.datetime.utcnow() + datetime.timedelta(hours=data.duration)
    order = Order(
        duration=data.duration,
        end_date=end_date,
        vending_machine_id=data.vending_machine_id,
        user_id=data.user_id,
    )

    session.add(order)
    vending_machine.rented = True

    await session.commit()
    await session.refresh(order)

    return OrdersDTO.model_validate(order)
