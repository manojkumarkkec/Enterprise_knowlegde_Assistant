from pydantic import BaseModel, ConfigDict, EmailStr, Field
from uuid import UUID


class RegisterRequest(BaseModel):

    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128,
    )


class UserResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID
    email: EmailStr
    role: str