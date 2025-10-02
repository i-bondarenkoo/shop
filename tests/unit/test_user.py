import pytest
from application.crud.user import create_user_crud, get_user_by_id_crud
from application.models.user import UserOrm
from datetime import datetime


@pytest.mark.asyncio
async def test_create_user(make_user_data, session_test_db):
    user = await create_user_crud(
        user_data=make_user_data,
        session=session_test_db,
    )

    assert user is not None
    assert user.email == make_user_data.email
    assert user.username == make_user_data.username
    assert user.is_active == make_user_data.is_active
    assert isinstance(user, UserOrm)
    assert isinstance(user.id, int)
    assert isinstance(user.created_at, datetime)


@pytest.mark.asyncio
async def test_get_user_by_id(
    create_user_db,
    create_order_db,
    session_test_db,
):
    user = await get_user_by_id_crud(user_id=create_user_db.id, session=session_test_db)
    assert user is not None
    assert len(user.orders) == 1
