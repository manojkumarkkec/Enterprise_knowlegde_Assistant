def reciprocal_rank_fusion(
    results: list[list[dict]],
    k: int = 60,
) -> list[dict]:

    scores = {}

    documents = {}


    for result_list in results:

        for rank,item in enumerate(result_list):

            chunk_id = item.get(
                "chunk_id",
                item.get("id")
            )


            scores[chunk_id] = (
                scores.get(chunk_id,0)
                +
                1/(k+rank+1)
            )


            documents[chunk_id]=item


    ranked = sorted(
        documents.values(),
        key=lambda x:
            scores[
                x.get(
                    "chunk_id",
                    x.get("id")
                )
            ],
        reverse=True
    )


    return ranked