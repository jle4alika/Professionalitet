# Database — Слой работы с БД

SQLAlchemy 2.0 (async) + PostgreSQL / SQLite.

## Структура

```
database/
├── db.py           # Engine, session, Base, get_session
└── models/         # Модели
    ├── user.py
    ├── order.py
    ├── payment.py
    └── vending_machine.py
```

## Подключение

Используется `project_config.settings`:

- **PostgreSQL**: `postgresql+asyncpg://user:pass@host:port/dbname`
- **SQLite** (тесты): `sqlite+aiosqlite:///:memory:` — задаётся через `TEST_DATABASE_URL`

Сессия через dependency: `get_session()` → `db_session` в API.

## Модели

### User (`users`)

| Поле        | Тип         | Описание                |
|-------------|-------------|-------------------------|
| id          | int (PK)    | —                       |
| username    | str         | уникальный              |
| password    | str         | —                       |
| email       | str         | уникальный              |
| phone_number| str?        | —                       |
| first_name  | str?        | —                       |
| last_name   | str?        | —                       |
| balance     | float       | default 0               |
| status      | UserStatus  | tenant / landlord       |
| created_time| datetime    | —                       |
| updated_time| datetime    | —                       |
| orders      | Order[]     | связь                   |
| payments    | Payment[]   | связь                   |

### Order (`orders`)

| Поле             | Тип      | Описание           |
|------------------|----------|--------------------|
| id               | int (PK) | —                  |
| duration         | int      | часы аренды        |
| end_date         | datetime | дата окончания     |
| expired          | bool     | default False      |
| vending_machine_id| int (FK) | → vending_machines |
| user_id          | int (FK) | → users            |
| created_time     | datetime | —                  |
| updated_time     | datetime | —                  |
| vending_machine  | VendingMachine | связь  |
| payment          | Payment[]| связь              |
| user             | User     | связь              |

### Payment (`payments`)

| Поле         | Тип          | Описание        |
|--------------|--------------|-----------------|
| id           | int (PK)     | —               |
| amount       | float        | —               |
| currency     | str          | default "RUB"   |
| payment_method | PaymentMethod | SBP / CARD    |
| payment_type | PaymentType  | rent / extension|
| success      | bool         | default False   |
| order_id     | int (FK)     | → orders        |
| user_id      | int (FK)     | → users         |
| created_time | datetime     | —               |
| updated_time | datetime     | —               |
| order        | Order        | связь           |
| user         | User         | связь           |

### VendingMachine (`vending_machines`)

| Поле         | Тип      | Описание    |
|--------------|----------|-------------|
| id           | int (PK) | —           |
| title        | str      | —           |
| amount_in_hour | float  | руб/час     |
| rented       | bool     | default False |
| created_time | datetime | —           |
| updated_time | datetime | —           |
| orders       | Order[]  | связь       |

## Связи

```
User 1──* Order *──1 VendingMachine
  │   \    │
  │    \   * Payment
  *────\────
```

## Создание таблиц

Миграции Alembic:

```bash
alembic upgrade head
```

Программно (drop + create):

```python
from backend.database.db import async_main
await async_main()
```
