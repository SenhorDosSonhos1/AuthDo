from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    username: str | None = Field(default=None)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(
        min_length=5,
        max_length=16,
        description="A senha deve ter no mínimo 5 caracteres e no máximo 16 caracteres.",
    )
    confirm_password: str = Field(
        min_length=5,
        max_length=16,
        description="A senha deve ter no mínimo 5 caracteres e no máximo 16 caracteres.",
    )


class UserPatch(BaseModel):
    password: str | None = Field(
        min_length=5,
        max_length=16,
        description="A senha deve ter no mínimo 5 caracteres e no máximo 16 caracteres.",
    )
    confirm_password: str | None = Field(
        min_length=5,
        max_length=16,
        description="A senha deve ter no mínimo 5 caracteres e no máximo 16 caracteres.",
    )


class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
