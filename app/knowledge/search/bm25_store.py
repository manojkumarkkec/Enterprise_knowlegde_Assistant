import pickle
from pathlib import Path

from rank_bm25 import BM25Okapi


class BM25Store:

    async def __init__(
        self,
        path: str = "storage/bm25/index.pkl",
    ):

        self.path = Path(path)

        self.documents: list[dict] = []

        self.index = None


    def build(
        self,
        documents: list[dict],
    ):

        self.documents = documents


        tokenized_documents = [
            doc["content"]
            .lower()
            .split()
            for doc in documents
        ]


        self.index = BM25Okapi(
            tokenized_documents
        )


        self.save()



    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:


        if self.index is None:
            self.load()


        if self.index is None:
            return []


        tokens = (
            query
            .lower()
            .split()
        )


        scores = self.index.get_scores(
            tokens
        )


        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True,
        )


        results = []


        for idx, score in ranked[:top_k]:

            results.append(
                {
                    **self.documents[idx],
                    "bm25_score": float(score),
                }
            )


        return results



    def save(self):

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )


        with open(
            self.path,
            "wb",
        ) as f:

            pickle.dump(
                {
                    "documents": self.documents,
                    "index": self.index,
                },
                f,
            )



    def load(self):

        if not self.path.exists():
            return


        with open(
            self.path,
            "rb",
        ) as f:

            data = pickle.load(f)


        self.documents = (
            data["documents"]
        )

        self.index = (
            data["index"]
        )