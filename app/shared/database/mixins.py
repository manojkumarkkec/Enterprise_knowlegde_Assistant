# TimestampMixin, UUIDMixin
from datetime import datetime, UTC
from uuid import UUID, uuid4

from sqlalchemy import Uuid
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column


class UUIDMixin:
    """Provides a UUID primary key."""

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
    )


class TimestampMixin:
    """Provides audit timestamps."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC), #The function is called each time a new row is inserted.
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )