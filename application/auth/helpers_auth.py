from application.schemas.user import LoginUser


def create_pydantic_model(username: str) -> LoginUser:
    return LoginUser(
        username=username,
        password="",
    )
