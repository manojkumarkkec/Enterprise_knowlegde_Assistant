from sentence_transformers import SentenceTransformer

from app.knowledge.embeddings.base import EmbeddingProvider


class SentenceTransformerEmbedding(EmbeddingProvider):
    """
    Local embedding provider using Sentence Transformers.
    """

    def __init__(self) -> None:
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    async def embed_text(
        self,
        text: str,
    ) -> list[float]:

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    async def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()
    
    