from sqlalchemy import (
    ForeignKey,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.shared.database.base_model import BaseModel


class Conversation(BaseModel):

    __tablename__ = "conversations"


    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )


    title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )


    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


    user = relationship(
        "User",
        back_populates="conversations",
        lazy="selectin",
    )