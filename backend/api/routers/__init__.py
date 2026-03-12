from fastapi import APIRouter

from backend.api.routers.rent import router as rent_router
from backend.api.routers.payment import router as payment_router
from backend.api.routers.user import router as user_router
from backend.api.routers.order import router as order_router

main_router = APIRouter()

main_router.include_router(rent_router)
main_router.include_router(payment_router)
main_router.include_router(user_router)
main_router.include_router(order_router)

