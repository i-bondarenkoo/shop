from datetime import timedelta, datetime
import jwt
from application.core.config import settings
from application.schemas.user import CreateUser
from application.auth.token import token_type


def create_jwt(
    payload: dict,
    algorithm: str = settings.token.algorithm,
    key: str = settings.token.key,
    expires_minutes: int = settings.token.access_token_expire_minutes,
    expires_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expires_timedelta:
        expire = expires_timedelta + now
    else:
        expire = now + timedelta(minutes=expires_minutes)

    to_encode["exp"] = expire
    to_encode["iat"] = now
    token = jwt.encode(
        payload=to_encode,
        key=key,
        algorithm=algorithm,
    )
    return token


def decode_jwt(
    token: str,
    algorithm: str = settings.token.algorithm,
    key: str = settings.token.key,
):
    decode_token = jwt.decode(
        jwt=token,
        algorithms=[algorithm],
        key=key,
    )
    return decode_token


def create_access_token(user_data: CreateUser):
    payload: dict = {
        "username": user_data.username,
        "token_type": token_type.ACCESS,
        "email": user_data.email,
    }
    access_token = create_jwt(
        payload=payload,
        key=settings.token.key,
        algorithm=settings.token.algorithm,
        expires_minutes=settings.token.access_token_expire_minutes,
    )
    return access_token
