from sqlalchemy.ext.asyncio import AsyncSession

from app.knowledge.embeddings.sentence_transformer import (
    SentenceTransformerEmbedding,
)
from app.knowledge.enums import DocumentStatus
from app.knowledge.models.document_chunk import DocumentChunk
from app.knowledge.models.vector_embedding import VectorEmbedding
from app.knowledge.search.bm25_store import BM25Store
from app.knowledge.vectorstores.faiss_store import FAISSVectorStore


class IngestionService:
    """
    Handles document ingestion pipeline.

    Flow:

    Document
        |
        Extract text
        |
        Create chunks
        |
        Generate embeddings
        |
        Store embeddings (PostgreSQL)
        |
        Store vectors (FAISS)
        |
        Update BM25
        |
        Finish
    """

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

        self.embedding_service = SentenceTransformerEmbedding()
        self.vector_store = FAISSVectorStore()
        self.bm25_store = BM25Store()

    async def initialize(self):
        """
        Initialize vector stores.
        Call this once before processing documents.
        """

        # Adjust these methods according to your implementation
        await self.vector_store.load()
        self.bm25_store.load()

    async def process_document(
        self,
        document,
        chunks: list[str],
    ):
        db_chunks: list[DocumentChunk] = []

        try:

            # ---------------------------------
            # 1. Create document chunks
            # ---------------------------------

            for index, text in enumerate(chunks):

                chunk = DocumentChunk(
                    document_id=document.id,
                    chunk_index=index,
                    content=text,
                    token_count=len(text.split()),
                    embedding_status="processing",
                )

                self.session.add(chunk)
                db_chunks.append(chunk)

            # Generate chunk IDs
            await self.session.flush()

            # ---------------------------------
            # 2. Generate embeddings
            # ---------------------------------

            texts = [
                chunk.content
                for chunk in db_chunks
            ]

            embeddings = await (
                self.embedding_service.embed_documents(texts)
            )

            # ---------------------------------
            # 3. Store embeddings in PostgreSQL
            # ---------------------------------

            for chunk, embedding in zip(
                db_chunks,
                embeddings,
            ):

                vector_embedding = VectorEmbedding(
                    chunk_id=chunk.id,
                    embedding=embedding,
                )

                self.session.add(vector_embedding)

            await self.session.flush()

            # ---------------------------------
            # 4. Prepare FAISS metadata
            # ---------------------------------

            metadata = []

            for chunk in db_chunks:

                metadata.append(
                    {
                        "chunk_id": str(chunk.id),

                        "document_id": str(document.id),

                        "filename": document.original_filename,

                        "chunk_index": chunk.chunk_index,

                        "uploaded_by": str(
                            document.uploaded_by
                        ),

                        "department": document.department,

                        "is_public": document.is_public,
                    }
                )

            # ---------------------------------
            # 5. Store vectors in FAISS
            # ---------------------------------

            await self.vector_store.upsert(
                ids=[
                    str(chunk.id)
                    for chunk in db_chunks
                ],
                embeddings=embeddings,
                metadata=metadata,
            )

            await self.vector_store.save()

            # ---------------------------------
            # 6. Update BM25
            # ---------------------------------

            await self.update_bm25(db_chunks)

            # ---------------------------------
            # 7. Update statuses
            # ---------------------------------

            for chunk in db_chunks:
                chunk.embedding_status = "completed"

            document.status = DocumentStatus.INDEXED

            await self.session.commit()

        except Exception:

            await self.session.rollback()

            try:
                document.status = DocumentStatus.FAILED
                self.session.add(document)
                await self.session.commit()
            except Exception:
                await self.session.rollback()

            raise

    async def update_bm25(
        self,
        chunks: list[DocumentChunk],
    ):
        """
        Add newly ingested chunks to the BM25 index.
        """

        documents = [
            {
                "chunk_id": str(chunk.id),
                "document_id": str(chunk.document_id),
                "text": chunk.content,
            }
            for chunk in chunks
        ]

        self.bm25_store.build(
            documents=documents,
        )

        self.bm25_store.save()