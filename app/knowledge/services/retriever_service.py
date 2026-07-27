from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.knowledge.embeddings.sentence_transformer import (
    SentenceTransformerEmbedding,
)

from app.knowledge.models.document_chunk import (
    DocumentChunk,
)
from app.knowledge.models.document import Document
from app.knowledge.search.cross_encoder import CrossEncoderReranker
from app.knowledge.vectorstores.faiss_store import (
    FAISSVectorStore,
)
from app.knowledge.search.bm25_store import (
    BM25Store,
)

from app.knowledge.search.ranking import (
    reciprocal_rank_fusion,
)

class RetrieverService:
    """
    Retrieves relevant document chunks
    from vector store.
    """

    def __init__(
        self,
        session: AsyncSession,
    ):

        self.session = session

        self.embedding_service = (
            SentenceTransformerEmbedding()
        )

        self.vector_store = (
            FAISSVectorStore()
        )

        self.bm25_store = BM25Store()
        
        self.reranker = CrossEncoderReranker()


    async def similarity_search(
        self,
        question: str,
        user_id: str,
        department: str | None = None,
        top_k: int = 5,
    ) -> list[dict]:


    # -------------------------
    # 1. Semantic search
    # -------------------------

        query_embedding = await (
            self.embedding_service
            .embed_text(question)
        )


        faiss_results = await (
            self.vector_store
            .similarity_search(
            embedding=query_embedding,
            top_k=10,
            )
        )


    # -------------------------
    # 2. Keyword search
    # -------------------------

        bm25_results = (
            self.bm25_store.search(
            question,
            top_k=10,
            )
        )


    # -------------------------
    # 3. Merge using RRF
    # -------------------------

        merged_results = (
            reciprocal_rank_fusion(
                [
                faiss_results,
                bm25_results,
                ]
            )
        )


        final_results = []


    # -------------------------
    # 4. Load chunk content
    # -------------------------

        for item in merged_results[:top_k]:

            query = (
                select(DocumentChunk)
                .join(DocumentChunk.document)
                .where(
                    DocumentChunk.id ==
                    item["chunk_id"]
                )
                .where(
                    Document.uploaded_by ==
                    user_id
                )
            )


            if department:

                query = query.where(
                    Document.department ==
                    department
            )


            result = await self.session.execute(query)

            

            chunk = (
                result.scalar_one_or_none()
            )


            if not chunk:
                continue


            final_results.append(
                {
                    "content": chunk.content,

                    "metadata": {
                        **item.get(
                        "metadata",
                        {}
                        ),

                        "rrf_score": item[
                        "rrf_score"
                        ],
                    },
                }
            )


        reranked_results = (
            self.reranker.rerank(
                question,
                final_results,
                top_k,
            )
        )


        return reranked_results