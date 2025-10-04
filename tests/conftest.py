from pydantic import EmailStr
import pytest_asyncio
import pytest
import httpx
import asyncio
from application.main import app
from application.db.database import test_db_helper, db_helper
from application.models.user import UserOrm
from application.schemas.order import CreateOrder
from application.schemas.user import CreateUser
from application.db import Base
from sqlalchemy import delete
from application.crud.user import create_user_crud
from application.crud.order import create_order_crud
from application.schemas.order import OrderStatus


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """
    На Windows asyncio по умолчанию использует ProactorEventLoop,
    который ломается с asyncpg.
    Здесь переключаем на SelectorEventLoop.
    """
    if (
        asyncio.get_event_loop_policy().__class__.__name__
        == "WindowsProactorEventLoopPolicy"
    ):
        loop = asyncio.SelectorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as ac:
        yield ac


@pytest_asyncio.fixture(scope="function")
async def override_get_session():
    async with test_db_helper.session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest_asyncio.fixture(scope="function", autouse=True)
def setup_test_db_session():
    async def _override_get_session():
        async with test_db_helper.session_factory() as session:
            try:
                yield session
            finally:
                await session.close()

    app.dependency_overrides[db_helper.get_session] = _override_get_session
    yield
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def make_user_data():
    return CreateUser(
        email="test_user@example.com",
        username="test_user",
        is_active=True,
        password="user",
    )


@pytest_asyncio.fixture(scope="function")
async def user_factory(override_get_session):
    async def _create_user(
        email: EmailStr,
        username: str,
        password: str,
        is_active: bool = False,
    ):
        user_data = CreateUser(
            email=email,
            username=username,
            password=password,
            is_active=is_active,
        )
        return await create_user_crud(
            user_data=user_data,
            session=override_get_session,
        )

    return _create_user


@pytest_asyncio.fixture(scope="function")
async def order_factory(override_get_session):
    async def _create_order(
        user: UserOrm,
        status: OrderStatus = OrderStatus.created,
    ):
        order_data = CreateOrder(
            user_id=user.id,
            status=status,
        )
        return await create_order_crud(
            order_data=order_data,
            session=override_get_session,
        )

    return _create_order


@pytest_asyncio.fixture(autouse=True)
async def clean_db():
    """
    Очищает все таблицы тестовой БД после каждого теста.
    """
    yield
    async with test_db_helper.session_factory() as session:
        # после выполнения теста БД чистится
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(delete(table))
        await session.commit()
