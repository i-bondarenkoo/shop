from application.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, DateTime
from datetime import datetime
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from application.models.user import UserOrm
    from application.models.order_items import OrderItemOrm


class OrderOrm(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    total_price: Mapped[int] = mapped_column(Integer, nullable=False)
    creted_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    # relation
    user: Mapped["UserOrm"] = relationship("UserOrm", back_populates="orders")

    items: Mapped[list["OrderItemOrm"]] = relationship(
        "OrderItemOrm",
        back_populates="order",
        cascade="all, delete-orphan",
    )
