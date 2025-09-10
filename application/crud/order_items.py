from sqlalchemy.ext.asyncio import AsyncSession
from application.models.order_items import OrderItemOrm
from application.schemas.order_items import CreateOrderItem, UpdateOrderItem
from application.crud.product import get_product_by_id_crud
from application.crud.order import get_order_by_id_crud
from application.crud.order import OrderOrm
from sqlalchemy import select


async def create_order_item_crud(data_in: CreateOrderItem, session: AsyncSession):
    product = await get_product_by_id_crud(
        product_id=data_in.product_id, session=session
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
    data_in: UpdateOrderItem,
    session: AsyncSession,
):
    order = await get_order_by_id_crud(order_id=data_in.order_id, session=session)
    if order is None:
        return None
    product = await get_product_by_id_crud(
        product_id=data_in.product_id,
        session=session,
    )
    if product is None:
        return None
    stmt = (
        select(OrderItemOrm)
        .where(
            OrderItemOrm.order_id == data_in.order_id,
            OrderItemOrm.product_id == data_in.product_id,
        )
        .order_by(OrderItemOrm.id)
    )
    result = await session.execute(stmt)
    item = result.scalars().one_or_none()
    if item is not None:
        item.quantity = data_in.new_quantity
        item.price_at_order = item.quantity * product.price
    await session.flush()
    await session.refresh(item)
    new_price_at_order = await sum_price_at_order(
        order_id=data_in.order_id, session=session
    )
    order.total_price = new_price_at_order
    await session.commit()
    return item
