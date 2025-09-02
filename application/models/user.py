from datetime import datetime
from application.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Boolean, String, Integer, DateTime


class UserOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)
