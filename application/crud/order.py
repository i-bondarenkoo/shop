from sqlalchemy.ext.asyncio import AsyncSession
from application.models.order import OrderOrm
from application.models.order_items import OrderItemOrm
from application.schemas.order import CreateOrder, UpdateOrder
from application.crud.user import get_user_by_id_crud
from sqlalchemy import select
from sqlalchemy.orm import selectinload


async def create_order_crud(order_data: CreateOrder, session: AsyncSession):
    current_user = await get_user_by_id_crud(
        user_id=order_data.user_id, session=session
    )
    if not current_user:
        return None
    new_order = OrderOrm(**order_data.model_dump())
    session.add(new_order)
    await session.commit()
    await session.refresh(new_order)
    return new_order


async def get_order_by_id_crud(order_id: int, session: AsyncSession):
    stmt = (
        select(OrderOrm)
        .where(OrderOrm.id == order_id)
        .options(
            selectinload(OrderOrm.user),
            selectinload(OrderOrm.items).selectinload(OrderItemOrm.product),
        )
    )
    result = await session.execute(stmt)
    order = result.scalars().first()
    if order is None:
        return None
    return order


async def get_list_order_by_id_crud(
    session: AsyncSession, start: int = 0, stop: int = 3
):
    stmt = (
        select(OrderOrm)
        .order_by(OrderOrm.id)
        .options(
            selectinload(OrderOrm.user),
            selectinload(OrderOrm.items).selectinload(OrderItemOrm.product),
        )
        .offset(start)
        .limit(stop - start)
    )
    result = await session.execute(stmt)
    list_orders: list = result.scalars().all()
    return list_orders


async def update_order_status_crud(
    order_status: UpdateOrder, order_id: int, session: AsyncSession
):
    order = await session.get(OrderOrm, order_id)
    if order is None:
        return None
    data: dict = order_status.model_dump(exclude_unset=True)

    for key, value in data.items():
        if value is not None:
            setattr(order, key, value)
    await session.commit()
    await session.refresh(order)
    return order


async def delete_order_crud(order_id: int, session: AsyncSession):
    order = await session.get(OrderOrm, order_id)
    if order is None:
        return None
    await session.delete(order)
    await session.commit()
    return {"message": "Заказ удален"}
