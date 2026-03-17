"""
REST API для вендинговых аппаратов
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select

from backend.api.schemas.vending_machine import (
    VendingMachinesDTO,
    VendingMachinesAddDTO,
    VendingMachinesUpdateDTO,
)
from backend.api.schemas.common import MessageResponse
from backend.database.models import VendingMachine
from backend.api.dependencies.db_session import db_session

router = APIRouter(
    tags=["Вендинговые аппараты"],
    prefix="/vending-machines",
)


@router.get("/", response_model=list[VendingMachinesDTO])
async def get_vending_machines(
    session: db_session,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    rented: bool | None = None,
) -> list[VendingMachinesDTO]:
    """Список всех вендинговых аппаратов с пагинацией и фильтром по статусу аренды."""
    query = select(VendingMachine).offset(skip).limit(limit)

    if rented is not None:
        query = query.where(VendingMachine.rented == rented)

    result = await session.execute(query)
    machines = result.scalars().all()

    return [VendingMachinesDTO.model_validate(m) for m in machines]


@router.get("/{machine_id}", response_model=VendingMachinesDTO)
async def get_vending_machine(
    machine_id: int, session: db_session
) -> VendingMachinesDTO:
    """Получить вендинговый аппарат по ID."""
    query = select(VendingMachine).where(VendingMachine.id == machine_id)
    result = await session.execute(query)
    machine = result.scalar_one_or_none()

    if not machine:
        raise HTTPException(status_code=404, detail="Vending machine not found")

    return VendingMachinesDTO.model_validate(machine)


@router.post("/", response_model=VendingMachinesDTO, status_code=201)
async def create_vending_machine(
    data: VendingMachinesAddDTO, session: db_session
) -> VendingMachinesDTO:
    """Создать новый вендинговый аппарат."""
    machine = VendingMachine(**data.model_dump())
    session.add(machine)

    await session.commit()
    await session.refresh(machine)

    return VendingMachinesDTO.model_validate(machine)


@router.patch("/{machine_id}", response_model=VendingMachinesDTO)
async def update_vending_machine(
    machine_id: int, data: VendingMachinesUpdateDTO, session: db_session
) -> VendingMachinesDTO:
    """Обновить вендинговый аппарат."""
    query = select(VendingMachine).where(VendingMachine.id == machine_id)
    result = await session.execute(query)
    machine = result.scalar_one_or_none()
    if not machine:
        raise HTTPException(status_code=404, detail="Vending machine not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(machine, key, value)

    await session.commit()
    await session.refresh(machine)

    return VendingMachinesDTO.model_validate(machine)


@router.delete("/{machine_id}", response_model=MessageResponse)
async def delete_vending_machine(
    machine_id: int, session: db_session
) -> MessageResponse:
    """Удалить вендинговый аппарат."""
    query = select(VendingMachine).where(VendingMachine.id == machine_id)
    result = await session.execute(query)
    machine = result.scalar_one_or_none()

    if not machine:
        raise HTTPException(status_code=404, detail="Vending machine not found")

    await session.delete(machine)
    await session.commit()

    return MessageResponse(message="Вендинговый аппарат успешно удалён")
