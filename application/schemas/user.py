from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application.schemas.order import ResponseOrder


class CreateUser(BaseModel):
    email: EmailStr
    username: str
    is_active: bool | None = False
    password: str


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class ResponseUser(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool | None = False
    # created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ResponseUserWithOrder(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool | None = False
    orders: list["ResponseOrder"]
    model_config = ConfigDict(from_attributes=True)


class UpdateUser(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
