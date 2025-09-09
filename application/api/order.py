from application.db.database import db_helper
from fastapi import Depends, HTTPException, Path, Body, Query, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from application.schemas.order import CreateOrder, ResponseOrder, UpdateOrder
from typing import Annotated
from application.crud.order import (
    create_order_crud,
    delete_order_crud,
    get_order_by_id_crud,
    get_list_order_by_id_crud,
    update_order_status_crud,
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post("/", response_model=ResponseOrder, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: Annotated[CreateOrder, Body(description="Данные для создания заказа")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    current_user = await create_order_crud(order_data=order_data, session=session)
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь указанный в заказе не существует",
        )
    return current_user


@router.get("/{order_id}", response_model=ResponseOrder)
async def get_order_by_id(
    order_id: Annotated[
        int, Path(gt=0, description="ID заказа для получения детальной информации")
    ],
    session: AsyncSession = Depends(db_helper.get_session),
):
    order = await get_order_by_id_crud(order_id=order_id, session=session)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не существует",
        )
    return order


@router.get("/", response_model=list[ResponseOrder])
async def get_list_orders(
    start: int = Query(0, ge=0, description="Начальный диапазон списка заказов"),
    stop: int = Query(3, gt=1, description="Конечный диапазон списка заказов"),
    session: AsyncSession = Depends(db_helper.get_session),
):
    if start > stop:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Некорректный диапзон списка",
        )
    list_orders = await get_list_order_by_id_crud(
        start=start, stop=stop, session=session
    )
    return list_orders


@router.patch("/{order_id}", response_model=ResponseOrder)
async def update_order_status(
    order_status: Annotated[
        UpdateOrder, Body(description="Поля для обновления заказа")
    ],
    order_id: Annotated[int, Path(gt=0, description="ID заказа для обновления")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    order = await get_order_by_id(order_id=order_id, session=session)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден",
        )
    data = order_status.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Статус для обновления заказа не передан",
        )
    return await update_order_status_crud(
        order_status=order_status,
        order_id=order_id,
        session=session,
    )


@router.delete("/{order_id}")
async def delete_order(
    order_id: Annotated[
        int, Path(gt=0, description="ID заказа, который нужно удалить")
    ],
    session: AsyncSession = Depends(db_helper.get_session),
):
    order = await delete_order_crud(order_id=order_id, session=session)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ не найден",
        )
    return order
