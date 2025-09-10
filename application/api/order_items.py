from fastapi import APIRouter, HTTPException, status, Path, Body, Query, Depends
from application.db.database import db_helper
from sqlalchemy.ext.asyncio import AsyncSession
from application.schemas.order_items import (
    CreateOrderItem,
    ResponseOrderItem,
    UpdateOrderItem,
)
from application.crud.order_items import create_order_item_crud, update_item_crud
from typing import Annotated

router = APIRouter(
    prefix="/order_items",
    tags=["OrderItems"],
)


@router.post("/", response_model=ResponseOrderItem, status_code=status.HTTP_201_CREATED)
async def create_order_item(
    data_in: Annotated[
        CreateOrderItem, Body(description="Данные для добавления новой позиции в заказ")
    ],
    session: AsyncSession = Depends(db_helper.get_session),
):

    order_item = await create_order_item_crud(data_in=data_in, session=session)
    if order_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Продукт или заказ не найдены"
        )
    return order_item


@router.patch("/", response_model=ResponseOrderItem)
async def update_item(
    data_in: Annotated[UpdateOrderItem, Body(description="Данные для обновления")],
    session: AsyncSession = Depends(db_helper.get_session),
):
    order_item = await update_item_crud(
        data_in=data_in,
        session=session,
    )
    if order_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заказ или продукт не существует",
        )
    return order_item
