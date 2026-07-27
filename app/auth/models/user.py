from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base_model import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.auth.models.role import Role


class User(BaseModel):
    """
    Represents an application user.
    """

    __tablename__ = "users"

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    role_id: Mapped[str] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False,
    )

    role: Mapped["Role"] = relationship(
    "Role",
    back_populates="users",
    lazy="selectin",
    )

    documents = relationship(
    "Document",
    back_populates="user",
    lazy="selectin",)

    conversations = relationship(
    "Conversation",
    back_populates="user",
    cascade="all, delete-orphan",
    lazy="selectin",
    )