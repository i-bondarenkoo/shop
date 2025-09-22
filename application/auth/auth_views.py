from fastapi import APIRouter, Depends, Body, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from application.schemas.user import CreateUser
from application.schemas.token import TokenResponse
from sqlalchemy.ext.asyncio import AsyncSession
from application.db.database import db_helper
from application.crud.user import create_user_crud
from application.auth.jwt import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

oauth2scheme = OAuth2PasswordBearer(tokenUrl="/auth/register")


# @router.post("/register", response_model=TokenResponse)
# async def register_user(
#     user_data: Annotated[
#         CreateUser, Body(description="Данные пользователя для регистрации")
#     ],
#     session: AsyncSession = Depends(db_helper.get_session),
# ):
#     user = await create_user_crud(user_data=user_data, session=session)
#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Пользователь не зарегистрирован в системе",
#         )
#     token = create_access_token(payload=)
