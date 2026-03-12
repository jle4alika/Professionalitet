from fastapi import APIRouter
from backend.api.schemas.user import *
from backend.api.schemas.order import *
from backend.api.schemas.payment import *
from backend.api.schemas.vending_machine import *

router = APIRouter(
    tags=["Пользователи"],
    prefix="/users",
)