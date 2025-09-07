from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class CreateProduct(BaseModel):
    name: str
    description: str
    price: float = Field(gt=0, description="Цена товара должна быть больше 0")
    stock_quantity: int = Field(gt=0, description="Количество на складе > 0")


class ResponseProduct(CreateProduct):
    id: int
    # created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UpdateProduct(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = Field(None, gt=0)
    stock_quantity: int | None = Field(None, gt=0)
