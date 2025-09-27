import pytest_asyncio
from application.schemas.user import CreateUser
from application.db.database import test_db_helper
from application.crud.user import create_user_crud


# фикстура создания пользователя(сам объект)
@pytest_asyncio.fixture
async def make_user_data():
    user = CreateUser(
        email="john@example.com",
        username="john_tavares",
        is_active=True,
        password="john",
    )
    return user


@pytest_asyncio.fixture
async def make_user_data_2():
    user = CreateUser(
        email="john@example.com",
        username="johnny",
        is_active=False,
        password="johnny",
    )
    return user


# функция создания сессии для подключение к БД
@pytest_asyncio.fixture
async def session_test_db():
    async for session in test_db_helper.get_session():
        try:
            yield session
        finally:
            await session.rollback()
            # await session.close()


# crud функция которая создаст строку в тестовой БД
@pytest_asyncio.fixture
async def create_user_db(make_user_data, session_test_db):
    new_user = await create_user_crud(
        user_data=make_user_data,
        session=session_test_db,
    )
    return new_user
