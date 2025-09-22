from enum import Enum


class TokenType(str, Enum):
    ACCESS = "ACCESS_TOKEN"
    REFRESH = "REFRESH_TOKEN"


token_type = TokenType()
