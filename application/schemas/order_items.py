from pydantic import BaseModel, ConfigDict, Field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application.schemas.product import ResponseProduct


class CreateOrderItem(BaseModel):
    product_id: int
    order_id: int
    quantity: int


class ResponseOrderItem(CreateOrderItem):
    id: int
    price_at_order: float
    model_config = ConfigDict(from_attributes=True)


class ResponseOrderItemWithOutProductID(BaseModel):
    order_id: int
    quantity: int
    id: int
    price_at_order: float
    model_config = ConfigDict(from_attributes=True)


class ResponseOrderItemWithOutID(BaseModel):
    id: int
    order_id: int
    quantity: int
    product: "ResponseProduct"
    price_at_order: float
    model_config = ConfigDict(from_attributes=True)


class UpdateOrderItem(BaseModel):
    new_quantity: int
