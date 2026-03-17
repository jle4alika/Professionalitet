# Backend — Сервис аренды вендинговых аппаратов

FastAPI + SQLAlchemy (async) + PostgreSQL / SQLite.

## Быстрый старт

```bash
pip install -r requirements.txt
# Создайте .env с DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME
alembic upgrade head
uvicorn backend.api.main:app --reload --port 8000
```

API: http://localhost:8000/docs

## Структура

```
backend/
├── api/                 # REST API
│   ├── main.py          # Точка входа
│   ├── routers/         # Эндпоинты (users, orders, payments, rents, vending-machines)
│   ├── schemas/         # Pydantic DTO
│   └── dependencies/    # DI (db_session)
├── database/            # Работа с БД
│   ├── db.py            # Engine, session, Base
│   └── models/          # SQLAlchemy модели (User, Order, Payment, VendingMachine)
├── migrations/          # Alembic миграции
└── tests/               # Pytest тесты
```

Подробнее об API: [api/README.md](api/README.md)

## Установка

```bash
pip install -r requirements.txt
```

## Конфигурация

Переменные окружения (`.env` в корне проекта):

| Переменная   | Описание    | По умолчанию |
|-------------|-------------|--------------|
| DB_HOST     | Хост БД     | localhost    |
| DB_PORT     | Порт        | 5432         |
| DB_USER     | Пользователь| postgres     |
| DB_PASS     | Пароль      | postgres     |
| DB_NAME     | Имя БД      | professionalitet |
| TEST_DATABASE_URL | URL тестовой БД | sqlite+aiosqlite:///:memory: |

## Запуск

```bash
# Из корня проекта
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

Документация: http://localhost:8000/docs

## Миграции

```bash
# Создать миграцию
alembic revision --autogenerate -m "описание"

# Применить
alembic upgrade head
```

## Тесты

```bash
# Из корня проекта
pytest backend/tests/ -v

# С PostgreSQL
TEST_DATABASE_URL=postgresql+asyncpg://user:pass@localhost/testdb pytest backend/tests/ -v
```

По умолчанию тесты используют SQLite in-memory.

## Стек

- **FastAPI** — веб-фреймворк
- **SQLAlchemy 2.0** — ORM (async)
- **Pydantic** — валидация и сериализация
- **AuthX** — JWT-авторизация
- **Alembic** — миграции БД
- **pytest + pytest-asyncio + httpx** — тесты
