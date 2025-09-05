from application.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, Numeric
from datetime import datetime

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application.models.order_items import OrderItemOrm


class ProductOrm(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(50), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # relation
    items: Mapped[list["OrderItemOrm"]] = relationship(
        "OrderItemOrm",
        back_populates="product",
        cascade="all, delete-orphan",
    )
