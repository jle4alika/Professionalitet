import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, EmailStr

from backend.database.models.user import UserStatus


class UsersAddDTO(BaseModel):
    username: str
    password: str
    email: EmailStr
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    status: Optional[str] = None


class UsersDTO(BaseModel):
    id: int
    username: str
    email: str
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    balance: float = 0
    status: Optional[UserStatus] = None
    created_time: datetime.datetime
    updated_time: datetime.datetime

    model_config = {"from_attributes": True}


class UsersRelOrdersDTO(UsersDTO):
    orders: List["OrdersDTO"]


class UsersRelPaymentsDTO(UsersDTO):
    payments: List["PaymentsDTO"]


class UsersUpdateDTO(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    balance: Optional[float] = None
    status: Optional[str] = None  # "tenant" | "landlord"


class UsersLoginDTO(BaseModel):
    username: str
    password: str
