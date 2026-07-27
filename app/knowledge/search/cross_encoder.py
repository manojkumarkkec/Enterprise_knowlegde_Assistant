from sentence_transformers import CrossEncoder


class CrossEncoderReranker:


    def __init__(self):

        self.model = CrossEncoder(
            "BAAI/bge-reranker-base"
        )


    def rerank(
        self,
        question: str,
        documents: list[dict],
        top_k: int = 5,
    ) -> list[dict]:


        if not documents:
            return []


        pairs = [
            (
                question,
                doc["content"],
            )
            for doc in documents
        ]


        scores = self.model.predict(
            pairs
        )


        ranked = []


        for doc, score in zip(
            documents,
            scores,
        ):

            doc["rerank_score"] = float(
                score
            )

            ranked.append(doc)



        ranked.sort(
            key=lambda x: x["rerank_score"],
            reverse=True,
        )


        return ranked[:top_k]