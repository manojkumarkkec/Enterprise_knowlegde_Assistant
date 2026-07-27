from sqlalchemy import (
    ForeignKey,
    Integer,
    Text,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.shared.database.base_model import BaseModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.knowledge.models.document import Document
    from app.knowledge.models.vector_embedding import VectorEmbedding


class DocumentChunk(BaseModel):
    """
    Stores extracted text chunks from documents.
    """

    __tablename__ = "document_chunks"


    document_id: Mapped[str] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False,
    )


    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )


    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )


    token_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )


    embedding_status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False,
    )


    document: Mapped["Document"] = relationship(
        "Document",
        back_populates="chunks",
        lazy="selectin",
    )

    embedding: Mapped["VectorEmbedding | None"] = relationship(
    "VectorEmbedding",
    back_populates="chunk",
    uselist=False,
    cascade="all, delete-orphan",
    lazy="selectin",
    )