from fastapi import FastAPI
import uvicorn
from application.core.config import settings


app = FastAPI(title="Mini-shop API")


if __name__ == "__main__":
    uvicorn.run(
        "application.main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
