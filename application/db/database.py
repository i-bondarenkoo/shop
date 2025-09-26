from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
)
from application.core.config import settings


class DatabaseHelper:

    def __init__(self, db_url: str):
        self.engine: AsyncEngine = create_async_engine(
            url=db_url,
            echo=settings.db_echo,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    async def close_connection(self):
        if self.engine is not None:
            return await self.engine.dispose()

    async def get_session(self):
        async with self.session_factory() as session:
            yield session


db_helper = DatabaseHelper(settings.db_url)
test_db_helper = DatabaseHelper(settings.test_db_url)
