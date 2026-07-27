class RetrievalMetrics:


    def precision_at_k(
        self,
        retrieved,
        relevant,
        k=5,
    ):

        retrieved_ids = [
            x["chunk_id"]
            for x in retrieved[:k]
        ]


        hits = len(
            set(retrieved_ids)
            &
            set(relevant)
        )


        return hits / k