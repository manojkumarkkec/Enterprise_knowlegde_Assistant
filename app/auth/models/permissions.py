from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base_model import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.auth.models.role import Role

class Permission(BaseModel):

    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    roles: Mapped[list["Role"]] = relationship(
    secondary="role_permissions",
    back_populates="permissions",
    lazy="selectin",
    )