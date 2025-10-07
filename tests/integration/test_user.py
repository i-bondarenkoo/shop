import json
import pytest
from datetime import datetime

from sqlalchemy.orm import selectinload
from application.models.user import UserOrm
from sqlalchemy import select
from application.models.order import OrderOrm
from application.schemas.order import OrderStatus
from application.schemas.user import LoginUser, UpdateUser
from tests.conftest import helper_make_user_schema


@pytest.mark.asyncio
async def test_create_user(
    client,
    make_user_data,
    override_get_session,
):
    response = await client.post(
        "/users/",
        # преобразуем pydantic -> dict
        # и отправляем запрос
        # httpx берет этот словарь и сериализует в json
        json=make_user_data.model_dump(),
    )
    assert response.status_code == 201
    # преобразуем json  в словарь
    data = response.json()
    assert data["email"] == make_user_data.email
    assert data["username"] == make_user_data.username
    assert data["is_active"] == make_user_data.is_active

    stmt = select(UserOrm).where(UserOrm.username == data["username"])
    result = await override_get_session.execute(stmt)
    user = result.scalars().one_or_none()
    assert user is not None
    assert isinstance(user.id, int)
    assert isinstance(user.created_at, datetime)
    assert user.hashed_password != make_user_data.password


@pytest.mark.asyncio
async def test_get_user_by_id(
    client,
    user_factory,
    order_factory,
):
    user = await user_factory(
        email="user@example.com",
        username="user1",
        password="pass",
        is_active=True,
    )
    order = await order_factory(
        user=user,
        status=OrderStatus.packed,
    )

    response = await client.get(
        f"/users/{user.id}",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user.username
    assert data["email"] == user.email
    assert data["is_active"] == user.is_active
    assert len(data["orders"]) == 1
    assert isinstance(data["orders"], list)
    assert isinstance(data["orders"][0], dict)
    assert data["orders"][0]["status"] == order.status
    assert data["orders"][0]["user_id"] == user.id


@pytest.mark.asyncio
async def test_get_list_user_by_id(
    client,
    order_factory,
    user_factory,
):
    user = await user_factory(
        email="user@example.com",
        username="user",
        password="pass1",
        is_active=True,
    )
    user2 = await user_factory(
        email="user2@example.com",
        username="user2",
        password="pass2",
        is_active=True,
    )
    user3 = await user_factory(
        email="user3@example.com",
        username="user3",
        password="pass3",
        is_active=False,
    )
    order = await order_factory(
        user=user,
        status=OrderStatus.packed,
    )
    order2 = await order_factory(
        user=user2,
        status=OrderStatus.created,
    )
    order3 = await order_factory(
        user=user,
        status=OrderStatus.paid,
    )
    response = await client.get(f"/users/?start=0&stop=3")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["username"] == user.username
    assert data[1]["username"] == user2.username
    assert data[2]["username"] == user3.username
    assert isinstance(data[0]["orders"], list)
    assert isinstance(data[0], dict)
    assert len(data) == 3
    # заказы
    assert len(data[0]["orders"]) == 2
    # количество ключей в словаре
    assert len(data[0]["orders"][0]) == 4
    assert len(data[1]["orders"]) == 1
    assert len(data[2]["orders"]) == 0
    assert data[0]["orders"][1]["status"] == OrderStatus.paid


@pytest.mark.asyncio
@pytest.mark.parametrize(
    # список имен параметров для теста
    "email, username",
    # сами параметры
    [
        ("new_user@example.com", None),
        (None, None),
        ("new_user@example.com", "new_user123"),
        (None, "new_user123"),
    ],
)
async def test_update_user(
    client,
    user_factory,
    email,
    username,
):
    user = await user_factory(
        email="user-email-test@example.com",
        username="user-test123",
        password="pass123",
    )
    update_user = UpdateUser(
        email=email,
        username=username,
    )
    response = await client.patch(
        f"/users/{user.id}",
        json=update_user.model_dump(),
    )
    data = response.json()
    if response.status_code == 400:
        assert data["detail"] == "Данные для обновление не переданы"
    else:
        assert response.status_code == 200
    if username is not None:
        assert data["username"] == username
        assert data["username"] != user.username
    if email is not None:
        assert data["email"] == email
        assert data["email"] != user.email


@pytest.mark.asyncio
async def test_delete_user(
    client,
    user_factory,
    order_factory,
    override_get_session,
):
    user = await user_factory(
        email="del-test@example.com",
        username="user333",
        password="test111",
    )
    order = await order_factory(
        user=user,
        status=OrderStatus.paid,
    )
    query = (
        select(UserOrm)
        .where(UserOrm.id == user.id)
        .options(
            selectinload(UserOrm.orders),
        )
    )
    result = await override_get_session.execute(query)
    user_db = result.scalars().first()
    assert user_db is not None
    assert isinstance(user_db, UserOrm)
    assert user_db.orders is not None
    response = await client.delete(f"/users/{user.id}")
    data = response.json()
    assert isinstance(data, dict)
    assert data == {"message": "Пользователь удален"}
    query_after_delete = select(UserOrm).where(UserOrm.id == user.id)
    more_result = await override_get_session.execute(query_after_delete)
    del_usr = more_result.scalars().one_or_none()
    assert del_usr is None


@pytest.mark.asyncio
async def test_login_user(
    client,
    user_factory,
):
    user = await user_factory(
        email="sam@example.com",
        username="sam-bones",
        is_active=True,
        password="sammy",
    )
    login_data = helper_make_user_schema(user=user, password="sammy")
    response = await client.post(
        f"/auth/login",
        data=login_data.model_dump(),
    )
    if response:
        assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert isinstance(data["access_token"], str)
    assert data["token_type"] == "Bearer"


@pytest.mark.asyncio
async def test_login_user_with_invalid_password(
    client,
    user_factory,
):
    user = await user_factory(
        email="andy@example.com",
        username="andy4351",
        is_active=True,
        password="andysupersecret",
    )
    login_data = helper_make_user_schema(user=user, password="invalid-test-pass")
    response = await client.post(
        "/auth/login",
        data=login_data.model_dump(),
    )
    assert response.status_code == 403
    data = response.json()
    assert data["detail"] == "Неверный логин или пароль"


@pytest.mark.asyncio
async def test_create_user_with_duplicate_email(
    client,
    make_user_data,
):
    response = await client.post(
        f"/users/",
        json=make_user_data.model_dump(),
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == make_user_data.username
    assert data["email"] == make_user_data.email

    second_response = await client.post(
        f"/users/",
        json=make_user_data.model_dump(),
    )
    assert second_response.status_code == 400
    second_data = second_response.json()
    assert second_data["detail"] == "Пользователь с такой почтой уже существует"
