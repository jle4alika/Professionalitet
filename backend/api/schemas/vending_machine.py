import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class VendingMachinesAddDTO(BaseModel):
    title: str
    amount_in_hour: float


class VendingMachinesUpdateDTO(BaseModel):
    title: Optional[str] = None
    amount_in_hour: Optional[float] = None
    rented: Optional[bool] = None


class VendingMachinesDTO(BaseModel):
    id: int
    title: str
    amount_in_hour: float
    rented: bool = False
    created_time: datetime.datetime
    updated_time: datetime.datetime

    model_config = {"from_attributes": True}


class VendingMachinesRelDTO(VendingMachinesDTO):
    orders: List["OrdersDTO"]
