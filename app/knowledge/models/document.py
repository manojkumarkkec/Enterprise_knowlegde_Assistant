from sqlalchemy import (
    ForeignKey,
    String,
    BigInteger,
    Enum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.shared.database.base_model import BaseModel
from app.knowledge.enums import DocumentStatus
from sqlalchemy import Boolean

if TYPE_CHECKING:
    from app.knowledge.models.document_chunk import DocumentChunk
    from app.auth.models.user import User

class Document(BaseModel):
    """
    Represents an uploaded document in the knowledge base.
    """

    __tablename__ = "documents"

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    content_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    storage_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    status: Mapped[DocumentStatus] = mapped_column(
        Enum(DocumentStatus),
        default=DocumentStatus.UPLOADED,
        nullable=False,
    )

    uploaded_by: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )


    user: Mapped["User"] = relationship(
        "User",
        back_populates="documents",
        lazy="selectin",
    )

    chunks: Mapped[list["DocumentChunk"]] = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    department: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )


    is_public: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )