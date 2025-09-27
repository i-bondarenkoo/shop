from datetime import datetime
import pytest
from application.utils import verify_password
from sqlalchemy.exc import IntegrityError
from application.crud.user import create_user_crud


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
