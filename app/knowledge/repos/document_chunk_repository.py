from sqlalchemy.ext.asyncio import AsyncSession

from app.knowledge.models.document_chunk import DocumentChunk


class DocumentChunkRepository:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session


    async def create_many(
        self,
        chunks: list[DocumentChunk],
    ):

        self.session.add_all(
            chunks
        )

        await self.session.flush()