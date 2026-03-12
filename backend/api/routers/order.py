from fastapi import APIRouter
from backend.api.schemas.user import *
from backend.api.schemas.order import *
from backend.api.schemas.payment import *
from backend.api.schemas.vending_machine import *

router = APIRouter(
    tags=["Заказы"],
    prefix="/orders",
)


@router.post("/")
async def create_order():
    return {"message": "Hello World"}

@router.get("/")
async def get_all_orders():
    return {"message": "Hello World"}

@router.post("/{order_id}")
async def create_order(order_id: int):
    return {"message": "Hello World"}