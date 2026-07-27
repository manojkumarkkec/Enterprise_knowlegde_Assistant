from abc import ABC, abstractmethod


class EmbeddingProvider(ABC):
    """
    Base interface for all embedding providers.
    """

    @abstractmethod
    async def embed_text(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a single text.
        """
        raise NotImplementedError

    @abstractmethod
    async def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """
        raise NotImplementedError