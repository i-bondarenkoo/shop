from fastapi import FastAPI
import uvicorn
from application.core.config import settings

app = FastAPI(title="Приложение магазин товаров")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
