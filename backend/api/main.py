import uvicorn
from fastapi import FastAPI, Response, HTTPException
from backend.api.routers import main_router
from fastapi.middleware.cors import CORSMiddleware
from authx.config import AuthXConfig
from authx import AuthX

app = FastAPI(
    title="API для сервиса аренды вендинговых аппаратов",
    description="REST API для управления пользователями, заказами, платежами и вендинговыми аппаратами",
    version="1.0.0",
)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(main_router)


@app.get("/")
async def root():
    """Корневой эндпоинт — информация об API."""
    return {
        "message": "API для сервиса аренды вендинговых аппаратов",
        "docs": "/docs",
        "api_v1": "/api/v1",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
