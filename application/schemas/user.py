from pydantic import BaseModel, ConfigDict, EmailStr


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
    model_config = ConfigDict(from_attributes=True)
