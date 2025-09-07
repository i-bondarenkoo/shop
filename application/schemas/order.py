from pydantic import BaseModel
from enum import Enum


class OrderStatus(str, Enum):
    created = "created"
    packed = "packed"
    paid = "paid"
