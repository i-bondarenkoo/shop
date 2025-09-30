import pytest_asyncio
import asyncio
import pytest
from application.schemas.order import CreateOrder
from application.schemas.user import CreateUser
from application.db.database import test_db_helper
from application.crud.user import create_user_crud
from application.crud.order import create_order_crud


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# фикстура создания пользователя(сам объект)
@pytest_asyncio.fixture(scope="function")
async def make_user_data():
    user = CreateUser(
        email="john@example.com",
        username="john_tavares",
        is_active=True,
        password="john",
    )
    return user


@pytest_asyncio.fixture(scope="function")
async def make_order_data(create_user_db):
    order = CreateOrder(
        status="packed",
        user_id=create_user_db.id,
    )
    return order


@pytest_asyncio.fixture(scope="function")
async def make_user_data_2():
    user = CreateUser(
        email="john@example.com",
        username="johnny",
        is_active=False,
        password="johnny",
    )
    return user


# функция создания сессии для подключение к БД
@pytest_asyncio.fixture(scope="function")
async def session_test_db():
    async with test_db_helper.session_factory() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


# crud функция которая создаст строку в тестовой БД
@pytest_asyncio.fixture(scope="function")
async def create_user_db(make_user_data, session_test_db):
    new_user = await create_user_crud(
        user_data=make_user_data,
        session=session_test_db,
    )
    return new_user


@pytest_asyncio.fixture(scope="function")
async def create_order_db(make_order_data, session_test_db):
    new_order = await create_order_crud(
        order_data=make_order_data,
        session=session_test_db,
    )
    return new_order
