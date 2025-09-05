from application.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, Numeric
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application.models.product import ProductOrm
    from application.models.order import OrderOrm


class OrderItemOrm(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_at_order: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    order: Mapped["OrderOrm"] = relationship("OrderOrm", back_populates="items")
    product: Mapped["ProductOrm"] = relationship("ProductOrm", back_populates="items")
