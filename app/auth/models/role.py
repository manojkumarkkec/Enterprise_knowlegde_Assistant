from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.auth.models.permissions import Permission
from app.shared.database.base_model import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.auth.models.permissions import Permission
    from app.auth.models.user import User

class Role(BaseModel):

    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    users: Mapped[list["User"]] = relationship(
    "User",
    back_populates="role",
    lazy="selectin",
    )


    permissions: Mapped[list["Permission"]] = relationship(
    secondary="role_permissions",
    back_populates="roles",
    lazy="selectin",
    )