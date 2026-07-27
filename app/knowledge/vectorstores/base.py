from abc import ABC, abstractmethod


class VectorStore(ABC):

    @abstractmethod
    async def upsert(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        metadata: list[dict],
    ) -> None:
        """
        Store or update an embedding.
        """
        raise NotImplementedError


    @abstractmethod
    async def similarity_search(
        self,
        embedding: list[float],
        top_k: int = 5,
    ) -> list[dict]:
        """
        Return the most similar chunks.
        """
        raise NotImplementedError
    
    @abstractmethod
    async def save(self) -> None:
        raise NotImplementedError


    @abstractmethod
    async def load(self) -> None:
        raise NotImplementedError