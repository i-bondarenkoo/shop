from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from application.models.order_items import OrderItemOrm
from application.schemas.order_items import CreateOrderItem, UpdateOrderItem
from application.crud.product import get_product_by_id_crud
from application.crud.order import get_order_by_id_crud
from application.models.order import OrderOrm
from application.models.product import ProductOrm
from sqlalchemy import select
from sqlalchemy.orm import selectinload


async def order_item_service(product_id: int, quantity: int, session: AsyncSession):
    # блокируем строку в БД до конца транзакции
    stmt = select(ProductOrm).where(ProductOrm.id == product_id).with_for_update()
    result = await session.execute(stmt)
    product = result.scalars().first()
    if product is None:
        return None
    if product.stock_quantity < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Товара в таком количестве нет на складе",
        )
    product.stock_quantity -= quantity
    return product


async def create_order_item_crud(data_in: CreateOrderItem, session: AsyncSession):

    product = await order_item_service(
        product_id=data_in.product_id,
        session=session,
        quantity=data_in.quantity,
    )
    if product is None:
        return None
    order = await get_order_by_id_crud(order_id=data_in.order_id, session=session)
    if order is None:
        return None
    order_item = OrderItemOrm(
        product_id=data_in.product_id,
        order_id=data_in.order_id,
        quantity=data_in.quantity,
        price_at_order=data_in.quantity * product.price,
    )
    session.add(order_item)
    await session.flush()
    await session.refresh(order_item)
    edit_price_in_order = await sum_price_at_order(
        order_id=order_item.order_id, session=session
    )
    order.total_price = edit_price_in_order
    await session.commit()
    return order_item


async def sum_price_at_order(order_id: int, session: AsyncSession):
    order = await session.get(OrderOrm, order_id)
    if order is None:
        return None
    stmt = (
        select(OrderItemOrm)
        .where(OrderItemOrm.order_id == order_id)
        .order_by(OrderItemOrm.id)
    )
    result = await session.execute(stmt)
    list_order_items = result.scalars().all()
    new_price_at_order = sum(elem.price_at_order for elem in list_order_items)
    order.total_price = new_price_at_order
    return order.total_price


async def update_item_crud(
    order_id: int,
    product_id: int,
    data_in: UpdateOrderItem,
    session: AsyncSession,
):
    order = await get_order_by_id_crud(order_id=order_id, session=session)
    if order is None:
        return None
    product = await get_product_by_id_crud(product_id=product_id, session=session)
    if product is None:
        return None
    item = await get_order_item_crud(
        order_id=order_id, product_id=product_id, session=session
    )
    change_price_and_quantity(
        item=item, new_quantity=data_in.new_quantity, product_price=product.price
    )
    order.total_price = await sum_price_at_order(order_id=order.id, session=session)
    await session.commit()
    return item


def change_price_and_quantity(
    item: OrderItemOrm, new_quantity: int, product_price: int
):
    item.quantity = new_quantity
    item.price_at_order = new_quantity * product_price


async def get_order_item_crud(order_id: int, product_id: int, session: AsyncSession):
    stmt = (
        select(OrderItemOrm)
        .where(
            OrderItemOrm.order_id == order_id,
            OrderItemOrm.product_id == product_id,
        )
        .options(
            selectinload(OrderItemOrm.product),
        )
        .order_by(OrderItemOrm.id)
    )
    result = await session.execute(stmt)
    item = result.scalars().one_or_none()

    return item


async def delete_order_item_crud(product_id: int, order_id: int, session: AsyncSession):
    item = await get_order_item_crud(
        product_id=product_id, order_id=order_id, session=session
    )
    if item is None:
        return None
    stmt = select(ProductOrm).where(ProductOrm.id == product_id).with_for_update()
    result = await session.execute(stmt)
    product = result.scalars().first()
    if product is None:
        return None
    product.stock_quantity += item.quantity
    await session.delete(item)
    await session.flush()
    order = await session.get(OrderOrm, order_id)
    if order:
        order.total_price = await sum_price_at_order(order_id=order_id, session=session)
    await session.commit()
    return {"message": "Продукт удален из заказа"}
