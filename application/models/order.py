from application.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, DateTime
from datetime import datetime
from typing import TYPE_CHECKING
from application.models.order_items import association_table

if TYPE_CHECKING:
    from application.models.user import UserOrm
    from application.models.product import ProductOrm


class OrderOrm(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    total_price: Mapped[int] = mapped_column(Integer, nullable=False)
    creted_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    # relation
    user: Mapped["UserOrm"] = relationship("UserOrm", back_populates="orders")

    products: Mapped[list["ProductOrm"]] = relationship(
        "ProductOrm",
        secondary=association_table,
        back_populates="orders",
    )
