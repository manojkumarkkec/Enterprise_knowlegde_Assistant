from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.knowledge.models.document import Document


class DocumentRepository:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session


    async def create(
        self,
        document: Document,
    ) -> Document:

        self.session.add(document)

        await self.session.flush()

        await self.session.refresh(document)

        return document


    async def get_by_id(
        self,
        document_id: UUID,
    ) -> Document | None:

        result = await self.session.execute(
            select(Document)
            .where(Document.id == document_id)
        )

        return result.scalar_one_or_none()


    async def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Document]:

        result = await self.session.execute(
            select(Document)
            .offset(skip)
            .limit(limit)
        )

        return list(result.scalars().all())


    async def delete(
        self,
        document: Document,
    ) -> None:

        await self.session.delete(document)