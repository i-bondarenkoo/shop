from pydantic import ConfigDict, BaseModel


class TokenResponse(BaseModel):
    token_type: str = "Bearer"
    token: str
