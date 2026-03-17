import datetime
from typing import Optional

from pydantic import BaseModel, Field
from backend.database.models.payment import PaymentMethod, PaymentType


class PaymentsAddDTO(BaseModel):
    amount: float
    currency: Optional[str] = "RUB"
    payment_method: PaymentMethod
    payment_type: PaymentType
    order_id: int
    user_id: int


class PaymentsDTO(BaseModel):
    id: int
    amount: float
    currency: str = "RUB"
    payment_method: PaymentMethod
    payment_type: PaymentType
    success: bool = False
    order_id: int
    user_id: int
    created_time: datetime.datetime
    updated_time: datetime.datetime

    model_config = {"from_attributes": True}


class PaymentsUpdateDTO(BaseModel):
    success: Optional[bool] = None


class PaymentsRelOrders(PaymentsDTO):
    order: "OrdersDTO"


class PaymentsRelUsers(PaymentsDTO):
    user: "UsersDTO"
