from fastapi import APIRouter
from backend.api.schemas.user import *
from backend.api.schemas.order import *
from backend.api.schemas.payment import *
from backend.api.schemas.vending_machine import *


router = APIRouter(
    tags=["Система оплат"],
    prefix="/payments",
)

@router.post("/")
async def create_payment():
    return {"message": "Hello World"}

@router.get("/")
async def get_all_payments():
    return {"message": "Hello World"}

@router.get("/check_payment{payment_id}")
async def check_payment(payment_id: int):
    return {"message": "Hello World"}

