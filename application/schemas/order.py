from pydantic import BaseModel, ConfigDict, Field
from enum import Enum


class OrderStatus(str, Enum):
    created = "created"
    packed = "packed"
    paid = "paid"
    canceled = "canceled"


class CreateOrder(BaseModel):
    status: OrderStatus
    user_id: int


class ResponseOrder(CreateOrder):
    id: int
    total_price: int
    # = Field(
    #     gt=0, description="Сумма заказа должна включать стоимость всех товаров"
    # )
    model_config = ConfigDict(from_attributes=True)


class UpdateOrder(BaseModel):
    status: OrderStatus | None = None
