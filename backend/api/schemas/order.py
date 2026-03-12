import datetime

from pydantic import BaseModel, Field

class OrdersAddDTO(BaseModel):
    duration: int

    vending_machine_id: int
    user_id: int

class OrdersDTO(OrdersAddDTO):
    id: int

    created_time: datetime.datetime
    updated_time: datetime.datetime

class OrdersRelVendingMachinesDTO(OrdersDTO):
    vending_machine: "VendingMachinesDTO"

class OrdersRelPaymentsDTO(OrdersDTO):
    payment: "PaymentsDTO"

class OrdersRelUsersDTO(OrdersDTO):
    user: "UsersDTO"






