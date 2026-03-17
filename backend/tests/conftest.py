"""
Pytest configuration and fixtures for async API tests.
"""

import os

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Set test database before any backend imports
# SQLite in-memory для тестов без PostgreSQL (можно переопределить TEST_DATABASE_URL)
os.environ.setdefault(
    "TEST_DATABASE_URL",
    "sqlite+aiosqlite:///:memory:",
)
os.environ.setdefault(
    "DB_NAME", os.environ.get("TEST_DB_NAME", "professionalitet_test")
)
os.environ.setdefault("DB_HOST", os.environ.get("DB_HOST", "localhost"))
os.environ.setdefault("DB_PORT", os.environ.get("DB_PORT", "5432"))
os.environ.setdefault("DB_USER", os.environ.get("DB_USER", "postgres"))
os.environ.setdefault("DB_PASS", os.environ.get("DB_PASS", "postgres"))

from backend.api.main import app
from backend.database.db import Base, engine, async_session
from backend.database.models import User, Order, Payment, VendingMachine


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    import asyncio

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def init_db():
    """Create tables before each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest_asyncio.fixture
async def client():
    """Async HTTP client for API tests."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        follow_redirects=True,
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def db_session():
    """Database session for test data setup."""
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def test_user(db_session):
    """Create a test user."""
    user = User(
        username="testuser",
        password="testpass123",
        email="test@example.com",
        first_name="Test",
        last_name="User",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest_asyncio.fixture
async def test_vending_machine(db_session):
    """Create a test vending machine."""
    vm = VendingMachine(title="Test Machine", amount_in_hour=100.0, rented=False)
    db_session.add(vm)
    await db_session.commit()
    await db_session.refresh(vm)
    return vm


@pytest_asyncio.fixture
async def test_order(db_session, test_user, test_vending_machine):
    """Create a test order."""
    import datetime

    user_id = test_user.id
    vm_id = test_vending_machine.id
    end_date = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    order = Order(
        duration=24,
        end_date=end_date,
        vending_machine_id=vm_id,
        user_id=user_id,
        expired=False,
    )
    db_session.add(order)
    vm = await db_session.get(VendingMachine, vm_id)
    if vm:
        vm.rented = True
    await db_session.commit()
    await db_session.refresh(order)
    return order


@pytest_asyncio.fixture
async def auth_client(client, test_user):
    """Get authenticated client (login first, cookies set automatically)."""
    response = await client.post(
        "/api/v1/users/login",
        json={"username": test_user.username, "password": test_user.password},
    )
    assert response.status_code == 200
    return client
