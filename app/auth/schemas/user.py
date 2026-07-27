from datetime import datetime
from uuid import UUID
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, AfterValidator

def verify_password_strength(v: str) -> str:
    """Validates that a password meets complexity rules."""
    if not any(c.isupper() for c in v):
        raise ValueError("must contain at least one uppercase letter")
    if not any(c.islower() for c in v):
        raise ValueError("must contain at least one lowercase letter")
    if not any(c.isdigit() for c in v):
        raise ValueError("must contain at least one digit")
    if not any(not c.isalnum() for c in v):
        raise ValueError("must contain at least one special character")
    return v

# Reusable modern type definition
PasswordField = Annotated[
    str, 
    Field(min_length=8, max_length=128), 
    AfterValidator(verify_password_strength)
]

class UserCreate(BaseModel):
    email: EmailStr
    password: PasswordField
    role_id: UUID



class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: EmailStr
    is_active: bool
    role_id: UUID
    created_at: datetime