from app.shared.database.base import Base
from app.shared.database.mixins import UUIDMixin, TimestampMixin


class BaseModel(UUIDMixin, TimestampMixin, Base):
    """
    Abstract base model for all ORM entities.
    Provides:
    - UUID primary key
    - created_at timestamp
    - updated_at timestamp
    """

    __abstract__ = True
    ROLE_NAME_MAX_LENGTH = 50
    DESCRIPTION_MAX_LENGTH = 255