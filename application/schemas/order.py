from pydantic import BaseModel, ConfigDict, Field
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application.schemas.user import ResponseUser
    from application.schemas.order_items import ResponseOrderItemWithOutID


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
    model_config = ConfigDict(from_attributes=True)


class UpdateOrder(BaseModel):
    status: OrderStatus | None = None


class ResponseOrderWithRelationship(BaseModel):
    id: int
    status: OrderStatus
    user: "ResponseUser"
    total_price: int
    items: list["ResponseOrderItemWithOutID"]
    model_config = ConfigDict(from_attributes=True)
