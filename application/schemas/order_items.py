from pydantic import BaseModel, ConfigDict, Field


class CreateOrderItem(BaseModel):
    product_id: int
    order_id: int
    quantity: int


class ResponseOrderItem(CreateOrderItem):
    id: int
    price_at_order: float
    model_config = ConfigDict(from_attributes=True)


class UpdateOrderItem(BaseModel):
    product_id: int
    order_id: int
    new_quantity: int
