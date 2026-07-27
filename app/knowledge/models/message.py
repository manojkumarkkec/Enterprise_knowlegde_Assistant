from sqlalchemy import (
    ForeignKey,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.shared.database.base_model import BaseModel


class Message(BaseModel):

    __tablename__ = "messages"


    conversation_id: Mapped[str] = mapped_column(
        ForeignKey("conversations.id"),
        nullable=False,
    )


    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )


    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )


    conversation = relationship(
        "Conversation",
        back_populates="messages",
    )