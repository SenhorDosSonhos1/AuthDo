from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, func, ForeignKey
from enum import Enum
from datetime import datetime

from app.models.user import User


class Todo(Base):
    __tablename__ = "todos"

    class StatusChoice(str, Enum):
        PENDING = "Pendente"
        COMPLETED = "Completo"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(155), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, default=None)
    status: Mapped[str] = mapped_column(
        String(10), default=StatusChoice.PENDING, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    user: Mapped["User"] = relationship()

    def __repr__(self):
        return (
            f"Tarefa: {self.title} - Status: {self.status} - Usuario: {self.user.email}"
        )
