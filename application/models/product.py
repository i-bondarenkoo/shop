from application.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime
from datetime import datetime
from application.models.order_items import association_table
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application.models.order import OrderOrm


class ProductOrm(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(50), nullable=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # relation
    orders: Mapped[list["OrderOrm"]] = relationship(
        "OrderOrm",
        secondary=association_table,
        back_populates="products",
    )
