from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.knowledge.models.conversation import Conversation
from app.knowledge.models.message import Message


class ConversationRepository:


    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session



    async def create(
        self,
        user_id: str,
    ):

        conversation = Conversation(
            user_id=user_id,
        )

        self.session.add(
            conversation
        )

        await self.session.flush()

        return conversation



    async def add_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
    ):

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        self.session.add(
            message
        )


    async def get_history(
        self,
        conversation_id: str,
        limit: int = 10,
    ):


        result = await self.session.execute(

            select(Message)

            .where(
                Message.conversation_id
                ==
                conversation_id
            )

            .order_by(
                Message.created_at.desc()
            )

            .limit(limit)

        )


        messages = (
            result.scalars()
            .all()
        )


        return list(
            reversed(messages)
        )