import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr

class UsersAddDTO(BaseModel):
    username: str
    password: str
    email: EmailStr
    phone_number: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]

    status: Optional[str]

class UsersDTO(BaseModel):
    id: int

    created_time: datetime.datetime
    updated_time: datetime.datetime

class UsersRelOrdersDTO(UsersDTO):
    orders: List["OrdersDTO"]

class UsersRelPaymentsDTO(UsersDTO):
    payments: List["PaymentsDTO"]
