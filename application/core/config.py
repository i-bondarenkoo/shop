from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class TokenConfig(BaseModel):
    algorithm: str = "HS256"
    key: str = "75a11ced7c40cd7232670caf2929279500d0ac354b1fc622b79c531c7f56aced"
    access_token_expire_minutes: int = 30


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="PARAMETRS_",
    )
    # DATABASE_URL = 'postgresql+asyncpg://user:password@localhost:5435/shop_app'
    # в env файле переменная должна называться так же как атрибут в классе, тогда pydantic автоматом будет искать эту перемнную(константу)
    # так же можно указать префикс тогда поиск префикс + имя атрибута
    db_url: str
    test_db_url: str
    db_echo: bool = True
    token: TokenConfig = TokenConfig()


settings = Settings()
