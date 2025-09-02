from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, PostgresDsn


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = "/api"


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
    db_echo: bool = True


settings = Settings()
