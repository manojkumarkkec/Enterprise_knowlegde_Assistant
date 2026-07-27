from app.shared.database.session import AsyncSessionLocal
from app.knowledge.services.document_processor import DocumentProcessor
from app.knowledge.repos.document_chunk_repository import DocumentChunkRepository


async def process_document(
    document_id,
):

    async with AsyncSessionLocal() as session:

        chunk_repository = DocumentChunkRepository(session)
        processor = DocumentProcessor(
            session
        )

        await processor.process(
            document_id,
            chunk_repository,
        )