import datetime
from typing import List

from pydantic import BaseModel, Field

class VendingMachinesAddDTO(BaseModel):
    title: str
    amount_in_hour: int

class VendingMachinesDTO(VendingMachinesAddDTO):
    id: int

    created_time: datetime.datetime
    updated_time: datetime.datetime

class VendingMachinesRelDTO(VendingMachinesDTO):
    orders: List["OrdersDTO"]
