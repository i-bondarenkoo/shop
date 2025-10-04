import pytest
from datetime import datetime
from application.models.user import UserOrm
from sqlalchemy import select
from application.models.order import OrderOrm
from application.schemas.order import OrderStatus
from application.schemas.user import ResponseUser


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
    # override_get_session,
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


# @pytest.mark.asyncio
# async def test_get_list_user_by_id(
#     create_user_db,
#     make_user_data,
#     make_user_data_2,
#     make_user_data_3,
#     override_get_session,
# ):
#     pass
