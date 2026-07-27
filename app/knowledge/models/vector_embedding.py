from typing import TYPE_CHECKING
from uuid import UUID

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.database.base_model import BaseModel


if TYPE_CHECKING:
    from app.knowledge.models.document_chunk import DocumentChunk



class VectorEmbedding(BaseModel):
    """
    Stores vector embeddings for document chunks.
    """

    __tablename__ = "vector_embeddings"


    chunk_id: Mapped[UUID] = mapped_column(
        ForeignKey("document_chunks.id"),
        nullable=False,
        unique=True,
    )


    embedding: Mapped[list[float]] = mapped_column(
        Vector(384),
        nullable=False,
    )


    chunk: Mapped["DocumentChunk"] = relationship(
        "DocumentChunk",
        back_populates="embedding",
        lazy="selectin",
    )