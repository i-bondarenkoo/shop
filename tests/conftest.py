import pytest_asyncio
import asyncio
import pytest
from application.db.base import Base
from application.db.database import test_db_helper
from application.schemas.order import CreateOrder
from application.schemas.user import CreateUser
from application.crud.user import create_user_crud
from application.crud.order import create_order_crud


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


# --- Сессия для тестов ---
@pytest_asyncio.fixture(scope="function")
async def session_test_db():
    """
    Сессия для тестов. Все изменения откатываются после теста.
    """
    async with test_db_helper.session_factory() as session:
        yield session
        await session.rollback()


# --- Очистка БД после каждого теста ---
@pytest_asyncio.fixture(autouse=True)
async def clean_db(session_test_db):
    yield
    # очистка всех таблиц
    for table in reversed(Base.metadata.sorted_tables):
        await session_test_db.execute(table.delete())
    await session_test_db.commit()


# фикстура подготовки данных для создания пользователя
@pytest_asyncio.fixture(scope="function")
async def make_user_data():
    return CreateUser(
        email="test_user@example.com",
        username="test_user",
        is_active=True,
        password="test",
    )


@pytest_asyncio.fixture(scope="function")
async def create_user_db(make_user_data, session_test_db):
    user = await create_user_crud(user_data=make_user_data, session=session_test_db)
    return user


@pytest_asyncio.fixture(scope="function")
async def make_order_data(create_user_db):
    return CreateOrder(
        status="packed",
        user_id=create_user_db.id,
    )


@pytest_asyncio.fixture(scope="function")
async def create_order_db(make_order_data, session_test_db):
    order = await create_order_crud(order_data=make_order_data, session=session_test_db)
    return order
