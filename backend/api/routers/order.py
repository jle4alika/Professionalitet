"""
REST API для заказов (аренды)
"""

import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select

from backend.api.schemas.order import OrdersDTO, OrdersAddDTO, OrdersUpdateDTO
from backend.api.schemas.common import MessageResponse
from backend.database.models import Order, VendingMachine
from backend.api.dependencies.db_session import db_session

router = APIRouter(
    tags=["Заказы"],
    prefix="/orders",
)


@router.get("/", response_model=list[OrdersDTO])
async def get_orders(
    session: db_session,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    user_id: int | None = None,
    expired: bool | None = None,
) -> list[OrdersDTO]:
    """Список заказов с пагинацией и фильтрами."""
    query = select(Order).offset(skip).limit(limit)

    if user_id is not None:
        query = query.where(Order.user_id == user_id)
    if expired is not None:
        query = query.where(Order.expired == expired)

    result = await session.execute(query)
    orders = result.scalars().all()

    return [OrdersDTO.model_validate(o) for o in orders]


@router.get("/{order_id}", response_model=OrdersDTO)
async def get_order(order_id: int, session: db_session) -> OrdersDTO:
    """Получить заказ по ID."""
    query = select(Order).where(Order.id == order_id)
    result = await session.execute(query)
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return OrdersDTO.model_validate(order)


@router.post("/", response_model=OrdersDTO, status_code=201)
async def create_order(data: OrdersAddDTO, session: db_session) -> OrdersDTO:
    """Создать новый заказ на аренду."""
    # Проверка существования аппарата
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

    # Помечаем аппарат как арендованный
    vending_machine.rented = True

    await session.commit()
    await session.refresh(order)

    return OrdersDTO.model_validate(order)


@router.patch("/{order_id}", response_model=OrdersDTO)
async def update_order(
    order_id: int, data: OrdersUpdateDTO, session: db_session
) -> OrdersDTO:
    """Обновить заказ (продление или отметка истечения)."""
    query = select(Order).where(Order.id == order_id)
    result = await session.execute(query)
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    update_data = data.model_dump(exclude_unset=True)
    if "duration" in update_data:
        # Продление: сдвигаем end_date
        order.end_date = order.end_date + datetime.timedelta(
            hours=update_data["duration"]
        )
        order.duration += update_data["duration"]
        update_data.pop("duration")

    for key, value in update_data.items():
        setattr(order, key, value)

    # При expired=True освобождаем аппарат
    if order.expired:
        vm_query = select(VendingMachine).where(
            VendingMachine.id == order.vending_machine_id
        )
        vm_result = await session.execute(vm_query)
        vm = vm_result.scalar_one_or_none()
        if vm:
            vm.rented = False

    await session.commit()
    await session.refresh(order)

    return OrdersDTO.model_validate(order)


@router.delete("/{order_id}", response_model=MessageResponse)
async def delete_order(order_id: int, session: db_session) -> MessageResponse:
    """Удалить/отменить заказ."""
    query = select(Order).where(Order.id == order_id)
    result = await session.execute(query)
    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Освобождаем аппарат
    vm_query = select(VendingMachine).where(
        VendingMachine.id == order.vending_machine_id
    )
    vm_result = await session.execute(vm_query)
    vm = vm_result.scalar_one_or_none()

    if vm:
        vm.rented = False

    await session.delete(order)
    await session.commit()

    return MessageResponse(message="Заказ успешно удалён")
