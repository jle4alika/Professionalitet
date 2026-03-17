"""Общие схемы для ответов API"""

from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Ответ с сообщением об успехе операции."""

    success: bool = True
    message: str


class LoginResponse(BaseModel):
    """Ответ при авторизации/регистрации."""

    access_token: str
    user_id: int | None = None


class AuthCheckResponse(BaseModel):
    """Ответ проверки авторизации."""

    auth: bool = True


class PaymentCheckResponse(BaseModel):
    """Ответ проверки статуса платежа."""

    id: int
    success: bool


class AvailableMachineItem(BaseModel):
    """Элемент списка доступных аппаратов."""

    id: int
    title: str
    amount_in_hour: float
