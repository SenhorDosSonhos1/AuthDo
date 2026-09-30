from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class TodoBase(BaseModel):
    title: str = Field(
        min_length=5,
        max_length=155,
        description="O titulo deve ter no minimo 5 caracteres e no máximo 155 caracteres.",
    )
    description: str | None = None


class TodoCreate(TodoBase): ...


class TodoUpdate(TodoBase): ...


class TodoResponse(TodoBase):
    id: int
    status: str
    created_at: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)
