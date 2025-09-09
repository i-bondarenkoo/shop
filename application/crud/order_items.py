from sqlalchemy.ext.asyncio import AsyncSession
from application.models.order_items import OrderItemOrm
from application.schemas.order_items import CreateOrderItem
from application.crud.product import get_product_by_id_crud
from application.crud.order import get_order_by_id_crud


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
        price_at_order=order_item.quantity * product.price,
    )
    return order_item
