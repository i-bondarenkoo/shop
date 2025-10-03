import pytest_asyncio
import pytest
import httpx
import asyncio
from application.main import app
from application.db.database import test_db_helper, db_helper
from application.schemas.order import CreateOrder
from application.schemas.user import CreateUser
from application.db import Base
from sqlalchemy import delete
from application.crud.user import create_user_crud


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


# получение сессии для тестовой базы
@pytest_asyncio.fixture(scope="function")
async def override_get_session():
    async with test_db_helper.session_factory() as session:
        try:
            yield session
            await session.rollback()
        finally:
            await session.close()


# подмена сессии с основной на тестовую
# за счет app.dependency_overrides[db_helper.get_session] = _override_get_session
@pytest_asyncio.fixture(scope="function", autouse=True)
def setup_test_db_session():
    async def _override_get_session():
        async with test_db_helper.session_factory() as session:
            try:
                yield session
                await session.rollback()
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
async def create_user_db(override_get_session, make_user_data):
    user = await create_user_crud(
        user_data=make_user_data,
        session=override_get_session,
    )
    return user


@pytest.fixture(scope="function")
def make_order_data(create_user_db):
    return CreateOrder(
        status="packed",
        user_id=create_user_db.id,
    )


@pytest_asyncio.fixture(autouse=True)
async def clean_db():
    """
    Очищает все таблицы тестовой БД перед каждым тестом.
    """
    async with test_db_helper.session_factory() as session:
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(delete(table))
        await session.commit()
        yield
        # если нужно, можно очистить повторно после теста
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(delete(table))
        await session.commit()
