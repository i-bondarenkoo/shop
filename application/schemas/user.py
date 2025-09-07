from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime


class CreateUser(BaseModel):
    email: EmailStr
    username: str
    is_active: bool | None = False
    password: str


class ResponseUser(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool | None = False
    # created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UpdateUser(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
