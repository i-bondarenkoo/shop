from turtle import up
from fastapi import APIRouter, Depends, status, Body, Path, HTTPException, Query
from application.crud.user import (
    create_user_crud,
    get_user_by_id_crud,
    get_list_users_by_id_crud,
    update_user_crud,
    delete_user_crud,
)
from application.schemas.user import CreateUser, ResponseUser, UpdateUser
from typing import Annotated
from application.db.database import db_helper
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/", response_model=ResponseUser, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: Annotated[
        CreateUser, Body(description="Данные пользователя для создания объекта в БД")
    ],
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await create_user_crud(user_data=user_data, session=session)


@router.get(
    "/{user_id}",
    response_model=ResponseUser,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_id(
    user_id: Annotated[
        int, Path(gt=0, description="ID пользователя, для получения информации")
    ],
    session: AsyncSession = Depends(db_helper.get_session),
):
    user = await get_user_by_id_crud(user_id=user_id, session=session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден"
        )
    return user


@router.get("/", response_model=list[ResponseUser])
async def get_list_users_by_id(
    start: int = Query(0, ge=0, description="Начальный диапазон списка пользователей"),
    stop: int = Query(3, gt=1, description="Конечный диапазон списка пользователей"),
    session: AsyncSession = Depends(db_helper.get_session),
):
    if start > stop:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Некорректный диапазон списка",
        )
    users: list = await get_list_users_by_id_crud(
        start=start, stop=stop, session=session
    )

    return users


@router.patch("/{user_id}", response_model=ResponseUser)
async def update_user(
    user_data: Annotated[
        UpdateUser, Body(description="Поля для обновления сущности - user")
    ],
    user_id: Annotated[int, Path(gt=0, description="ID Пользователя для обновления")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    data: dict = user_data.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Данные для обновления не переданы",
        )
    user = await update_user_crud(user_data=user_data, user_id=user_id, session=session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: Annotated[int, Path(gt=0, description="ID Пользователя для удаления")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    user = await delete_user_crud(user_id=user_id, session=session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )
    return user
