from fastapi import APIRouter, Depends, Body, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr
from application.schemas.token import TokenResponse
from sqlalchemy.ext.asyncio import AsyncSession
from application.db.database import db_helper
from application.auth.jwt import create_access_token
from application.schemas.user import LoginUser
from application.crud.user import get_user_by_email_crud
router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

oauth2scheme = OAuth2PasswordBearer(tokenUrl="/auth/register")




@router.post("/login")
async def login_user(
    data: Annotated[
        LoginUser, Body(description="Данные для авторизации, логин и пароль")
    ],
    session: AsyncSession = Depends(db_helper.get_session),
):
    user = await get_user_by_email_crud(data=data, session=session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Неверный логин или пароль')
    token = 
