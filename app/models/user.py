from app.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, func
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(155), nullable=False)
    email: Mapped[str] = mapped_column(
        String(155), unique=True, nullable=False, index=True
    )
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp()
    )

    def __repr__(self):
        return f"User: {self.username} - Email: {self.email}"
