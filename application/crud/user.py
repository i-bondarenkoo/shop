from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from application.utils.security import hash_password
from application.schemas.user import CreateUser, LoginUser, UpdateUser
from application.models.user import UserOrm
from sqlalchemy import select
from sqlalchemy.orm import selectinload


async def create_user_crud(user_data: CreateUser, session: AsyncSession):
    new_user = UserOrm(
        email=user_data.email,
        username=user_data.username,
        is_active=user_data.is_active,
        hashed_password=hash_password(user_data.password),
    )
    session.add(new_user)
    await session.commit()
    # await session.flush()
    await session.refresh(new_user)
    return new_user


async def get_user_by_id_crud(user_id: int, session: AsyncSession):
    stmt = (
        select(UserOrm)
        .where(UserOrm.id == user_id)
        .options(
            selectinload(UserOrm.orders),
        )
    )
    result = await session.execute(stmt)
    user = result.scalars().first()
    if user is None:
        return None
    return user


async def get_list_users_by_id_crud(
    session: AsyncSession, start: int = 0, stop: int = 3
):
    stmt = (
        select(UserOrm)
        .order_by(UserOrm.id)
        .options(
            selectinload(
                UserOrm.orders,
            )
        )
        .offset(start)
        .limit(stop - start)
    )
    list_users_orm = await session.execute(stmt)
    users: list = list_users_orm.scalars().all()
    return users


async def update_user_crud(user_data: UpdateUser, user_id: int, session: AsyncSession):
    user = await get_user_by_id_crud(user_id=user_id, session=session)
    if user is None:
        return None
    # преобразуем данные из JSON в словарик питона
    data: dict = user_data.model_dump(exclude_unset=True)

    for key, value in data.items():
        if value is not None:
            setattr(user, key, value)
    await session.commit()
    await session.refresh(user)
    return user


async def delete_user_crud(user_id: int, session: AsyncSession):
    user = await session.get(UserOrm, user_id)
    if user is None:
        return None
    await session.delete(user)
    await session.commit()
    return {"message": "Пользователь удален"}


async def get_user_by_username_crud(data: LoginUser, session: AsyncSession):
    stmt = select(UserOrm).where(UserOrm.username == data.username)
    result = await session.execute(stmt)
    user = result.scalars().one_or_none()
    if user is None:
        return None
    return user


async def get_user_by_email(email: EmailStr, session: AsyncSession):
    stmt = select(UserOrm).where(UserOrm.email == email)
    result = await session.execute(stmt)
    user = result.scalars().one_or_none()
    if user is None:
        return None
    return user
