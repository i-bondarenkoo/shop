from datetime import datetime
import pytest
from application.models.order import OrderOrm
from application.models.user import UserOrm
from application.utils import verify_password
from sqlalchemy.exc import IntegrityError
from application.crud.user import create_user_crud, get_user_by_id_crud
from sqlalchemy import select


@pytest.mark.asyncio
async def test_create_user(
    make_user_data,
    session_test_db,
):
    user = await create_user_crud(
        user_data=make_user_data,
        session=session_test_db,
    )
    assert user is not None
    assert user.email == make_user_data.email
    assert user.username == make_user_data.username
    assert user.is_active == make_user_data.is_active
    assert user.hashed_password != make_user_data.password
    assert verify_password(make_user_data.password, user.hashed_password)
    assert isinstance(user.created_at, datetime)
    assert isinstance(user.id, int)
    # Попытка создать 2 пользователя с такой же почтой
    with pytest.raises(IntegrityError):
        await create_user_crud(
            user_data=make_user_data,
            session=session_test_db,
        )


@pytest.mark.asyncio
async def test_get_user_by_id(
    session_test_db,
    create_user_db,
    make_user_data,
    make_order_data,
    create_order_db,
):
    query = select(UserOrm).where(UserOrm.username == make_user_data.username)
    result = await session_test_db.execute(query)
    user = result.scalars().one_or_none()
    user_with_order = await get_user_by_id_crud(
        user_id=user.id,
        session=session_test_db,
    )
    assert user_with_order is not None
    assert user_with_order.username == make_user_data.username
    assert user_with_order.email == make_user_data.email
    assert user_with_order.orders[0].status == make_order_data.status
    assert user_with_order.orders[0].user_id == user_with_order.id
