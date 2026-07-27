from uuid import UUID
from app.knowledge.models.document_chunk import DocumentChunk
from app.knowledge.repos.document_chunk_repository import (
    DocumentChunkRepository,
)

from sqlalchemy.ext.asyncio import AsyncSession
from app.knowledge.repos.document_repository import DocumentRepository
from app.knowledge.enums import DocumentStatus
from app.knowledge.ingestion.extractor import DocumentExtractor
from app.knowledge.ingestion.chunker import TextChunker



class DocumentProcessor:

    def __init__(
    self,
    session: AsyncSession,
    ):

        self.repository = DocumentRepository(
        session
        )

        self.chunk_repository = DocumentChunkRepository(
        session
       )


    async def process(
        self,
        document_id: UUID,
        chunk_repository: DocumentChunkRepository,
    ):

        document = await self.repository.get_by_id(
            document_id
        )

        if document is None:
            return


        # Update status
        document.status = DocumentStatus.PROCESSING

        await self.repository.session.commit()


        try:

            extractor = DocumentExtractor()

            text = await extractor.extract(
              document.storage_path
            )


            if not text.strip():
                  raise ValueError(
                "No text extracted"
                )


            chunker = TextChunker()

            chunks = chunker.split(
                text
                )

            document_chunks = []


            for index, chunk in enumerate(chunks):
                document_chunk = DocumentChunk(
                    document_id=document.id,
                    chunk_index=index,
                    content=chunk,
                    embedding_status="pending",
                )
                document_chunks.append(document_chunk)


            await self.chunk_repository.create_many(document_chunks)

            document.status = DocumentStatus.CHUNKED

        except Exception as e:
            document.status = DocumentStatus.FAILED
            print(f"Document processing failed: {e}")
        finally:
            await self.repository.session.commit()