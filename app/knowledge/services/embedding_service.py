from typing import Sequence


class EmbeddingService:

    async def generate_embedding(
        self,
        text: str,
    ) -> Sequence[float]:
        raise NotImplementedError