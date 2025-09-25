from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Body, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from application.schemas.token import TokenResponse
from sqlalchemy.ext.asyncio import AsyncSession
from application.db.database import db_helper
from application.auth.jwt import create_access_token, decode_jwt
from application.schemas.user import ResponseUser
from application.crud.user import get_user_by_username_crud
from application.utils.security import verify_password
from application.core.config import settings
from application.auth.helpers_auth import create_pydantic_model

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

oauth2scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/login")
async def login_user(
    data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(db_helper.get_session),
):
    user_model = create_pydantic_model(username=data.username)
    user = await get_user_by_username_crud(data=user_model, session=session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Неверный логин или пароль"
        )
    password = verify_password(
        password=data.password,
        hashed_password=user.hashed_password,
    )
    if not password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Неверный логин или пароль"
        )

    token = create_access_token(user)
    return TokenResponse(
        token_type="Bearer",
        access_token=token,
    )


async def get_current_user(
    token: Annotated[str, Depends(oauth2scheme)],
    session: AsyncSession = Depends(db_helper.get_session),
):
    decode_token: dict = decode_jwt(
        token=token,
        algorithm=settings.token.algorithm,
        key=settings.token.key,
    )
    username = decode_token["username"]
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не авторизован",
        )
    user_model = create_pydantic_model(username=username)
    user_db = await get_user_by_username_crud(data=user_model, session=session)
    return user_db


@router.get("/me", response_model=ResponseUser)
async def read_user(user: Annotated[ResponseUser, Depends(get_current_user)]):
    return user
