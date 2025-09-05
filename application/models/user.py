from datetime import datetime
from application.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, String, Integer, DateTime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from application.models.order import OrderOrm


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)

    # relation
    orders: Mapped[list["OrderOrm"]] = relationship(
        "OrderOrm",
        back_populates="user",
        cascade="all, delete-orphan",
    )
