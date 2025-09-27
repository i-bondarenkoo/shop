from datetime import datetime
import pytest
from application.models.user import UserOrm
from application.utils import verify_password
from sqlalchemy.exc import IntegrityError
from application.crud.user import create_user_crud, get_user_by_id_crud


@pytest.mark.asyncio
async def test_create_user(
    create_user_db,
    session_test_db,
    make_user_data,
    make_user_data_2,
):
    assert create_user_db is not None
    assert create_user_db.created_at is not None
    assert isinstance(create_user_db.created_at, datetime)
    assert create_user_db.email == make_user_data.email
    assert create_user_db.username == make_user_data.username
    assert create_user_db.is_active == make_user_data.is_active
    assert verify_password(make_user_data.password, create_user_db.hashed_password)
    assert isinstance(create_user_db.id, int)
    # попытка создать 2 пользователя, чтобы проверить исключение
    with pytest.raises(IntegrityError):
        await create_user_crud(user_data=make_user_data_2, session=session_test_db)


@pytest.mark.asyncio
async def test_get_user_by_id(
    create_user_db,
    session_test_db,
    make_user_data,
    make_order_data,
    create_order_db,
):
    response = await get_user_by_id_crud(
        user_id=create_user_db.id,
        session=session_test_db,
    )
    assert response is not None
    assert isinstance(create_user_db.id, int)
    assert isinstance(response, UserOrm)
    assert response.username == make_user_data.username
    assert response.email == make_user_data.email

    # assert response.orders[0].status == make_order_data.status
    # assert response.orders[0].user_id == make_order_data.user_id
