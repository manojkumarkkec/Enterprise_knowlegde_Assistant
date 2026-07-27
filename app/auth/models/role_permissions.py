from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base


class RolePermission(Base):
    """
    Association table between roles and permissions.
    """

    __tablename__ = "role_permissions"

    role_id: Mapped[str] = mapped_column(
        ForeignKey("roles.id"),
        primary_key=True,
    )

    permission_id: Mapped[str] = mapped_column(
        ForeignKey("permissions.id"),
        primary_key=True,
    )