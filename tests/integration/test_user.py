import pytest
from datetime import datetime
from application.models.user import UserOrm
from sqlalchemy import select


@pytest.mark.asyncio
async def test_create_user(client, make_user_data, override_get_session):
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
async def test_get_user_by_id(client, create_user_db):
    response = await client.get(
        f"/users/{create_user_db.id}",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == create_user_db.username
    assert data["email"] == create_user_db.email
