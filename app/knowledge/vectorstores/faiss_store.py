from pathlib import Path

import faiss
import numpy as np
from pydantic import json

from app.knowledge.vectorstores.base import VectorStore


class FAISSVectorStore(VectorStore):

    def __init__(
        self,
        dimension: int = 384,
        index_path: str = "storage/faiss.index",
        metadata_path: str = "storage/faiss_metadata.json",
    ):

        self.dimension = dimension

        self.index_path = Path(index_path)

        self.metadata_path = Path(
            metadata_path
        )


        self.index = faiss.IndexFlatIP(
            dimension
        )

        # vector position -> metadata
        self.metadata: list[dict] = []

        self.ids: list[str] = []

        if self.index_path.exists():
            self.index = faiss.read_index(
                str(self.index_path)
            )



    async def upsert(
        self,
        ids: list[str],
        embeddings: list[list[float]],
        metadata: list[dict],
    ) -> None:

        vectors = np.array(
            embeddings,
            dtype=np.float32,
        )

        self.index.add(
            vectors
        )

        self.ids.extend(
            ids
        )

        start_id = len(self.metadata)


        for index, item in enumerate(metadata):

            item["vector_id"] = start_id + index

        self.metadata.extend(
            metadata
        )


    async def similarity_search(
        self,
        embedding: list[float],
        top_k: int = 5,
    ) -> list[dict]:

        vector = np.array(
            [embedding],
            dtype=np.float32,
        )

        distances, indexes = self.index.search(
            vector,
            top_k,
        )

        results: list[dict] = []

        for score, idx in zip(distances[0], indexes[0]):

            if idx == -1:
                continue

            results.append({
                "id": self.ids[idx],
                "score": float(score),
                "metadata": self.metadata[idx],
            })

        return results



    async def save(self):

        self.index_path.parent.mkdir(
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            str(self.index_path),
        )

        with open(
            self.metadata_path,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                self.metadata,
                f,
                indent=4,
            )



    async def load(self):

        if self.index_path.exists():

            self.index = faiss.read_index(
                str(self.index_path)
            )

        if self.metadata_path.exists():

            with open(
                self.metadata_path,
                "r",
                encoding="utf-8",
            ) as f:

                self.metadata = json.load(f)

        if self.index.ntotal != len(self.metadata):

            raise RuntimeError(
                "FAISS index and metadata count mismatch"
            )