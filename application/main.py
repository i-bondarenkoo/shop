from fastapi import FastAPI
import uvicorn
from application.core.config import settings
from application.api.user import router as user_router
from application.api.product import router as product_router
from application.api.order import router as order_router

app = FastAPI(title="Mini-shop API")
app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)
if __name__ == "__main__":
    uvicorn.run(
        "application.main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )
