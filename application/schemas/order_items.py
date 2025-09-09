from pydantic import BaseModel, ConfigDict


class CreateOrderItem(BaseModel):
    product_id: int
    order_id: int
    quantity: int


class ResponseOrderItem(CreateOrderItem):
    id: int
    price_at_order: float
    model_config = ConfigDict(from_attributes=True)
