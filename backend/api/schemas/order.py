import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class OrdersAddDTO(BaseModel):
    duration: int
    vending_machine_id: int
    user_id: int


class OrdersDTO(BaseModel):
    id: int
    duration: int
    end_date: datetime.datetime
    expired: bool = False
    vending_machine_id: int
    user_id: int
    created_time: datetime.datetime
    updated_time: datetime.datetime

    model_config = {"from_attributes": True}


class OrdersUpdateDTO(BaseModel):
    duration: Optional[int] = None
    expired: Optional[bool] = None


class OrdersRelVendingMachinesDTO(OrdersDTO):
    vending_machine: "VendingMachinesDTO"


class OrdersRelPaymentsDTO(OrdersDTO):
    payment: List["PaymentsDTO"]


class OrdersRelUsersDTO(OrdersDTO):
    user: "UsersDTO"
