import pytest
from application.models.user import UserOrm
from application.schemas.user import CreateUser, LoginUser
from application.crud.user import (
    create_user_crud,
    get_user_by_username_crud,
    get_user_by_email,
)


@pytest.fixture(scope="function")
def pydantic_user_data():
    return CreateUser(
        email="polly@mail.com",
        username="polly-molly",
        password="polly123",
    )


@pytest.mark.asyncio
async def test_get_user_by_username(
    pydantic_user_data,
    override_get_session,
):
    new_user = await create_user_crud(
        user_data=pydantic_user_data,
        session=override_get_session,
    )
    test_model = LoginUser(
        username=new_user.username,
        password=pydantic_user_data.password,
    )
    result = await get_user_by_username_crud(
        data=test_model, session=override_get_session
    )
    assert result is not None
    assert result.username == pydantic_user_data.username
    assert result.email == pydantic_user_data.email
    assert result.is_active == False
    assert isinstance(result, UserOrm)


@pytest.mark.asyncio
async def test_get_user_by_email(pydantic_user_data, override_get_session):
    new_user = await create_user_crud(
        user_data=pydantic_user_data,
        session=override_get_session,
    )
    result = await get_user_by_email(
        email=new_user.email,
        session=override_get_session,
    )
    assert result is not None
    assert result.username == pydantic_user_data.username
    assert result.email == pydantic_user_data.email
    assert result.is_active == False
    assert isinstance(result, UserOrm)
