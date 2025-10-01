from datetime import datetime
import pytest
from application.crud.order import create_order_crud
from application.models.order import OrderOrm
from application.models.user import UserOrm
from application.utils import verify_password
from sqlalchemy.exc import IntegrityError
from application.crud.user import create_user_crud, get_user_by_id_crud


# @pytest.mark.asyncio
# async def test_create_user(
#     make_user_data,
#     session_test_db,
# ):
#     user = await create_user_crud(
#         user_data=make_user_data,
#         session=session_test_db,
#     )
#     assert user is not None
#     assert user.email == make_user_data.email
#     assert user.username == make_user_data.username
#     assert user.is_active == make_user_data.is_active
#     assert user.hashed_password != make_user_data.password
#     assert verify_password(make_user_data.password, user.hashed_password)
#     assert isinstance(user.created_at, datetime)
#     assert isinstance(user.id, int)
#     # Попытка создать 2 пользователя с такой же почтой
#     with pytest.raises(IntegrityError):
#         await create_user_crud(
#             user_data=make_user_data,
#             session=session_test_db,
#         )


@pytest.mark.asyncio
async def test_get_user_by_id(
    create_user_db,
    create_order_db,
    session_test_db,
    make_user_data,
    make_order_data,
):
    user = await get_user_by_id_crud(
        user_id=create_user_db.id,
        session=session_test_db,
    )
    assert user is not None
    assert user.id == create_user_db.id
    assert user.email == create_user_db.email
    assert user.username == create_user_db.username
    assert isinstance(user, UserOrm)
    assert user.orders[0].status == make_order_data.status
