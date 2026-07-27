from app.knowledge.search.ranking import (
    reciprocal_rank_fusion,
)


def test_reciprocal_rank_fusion_merges_results():

    results = [

        # Vector search results
        [
            {
                "id": "doc1",
                "content": "Leave policy",
            },
            {
                "id": "doc2",
                "content": "Holiday policy",
            },
        ],

        # BM25 search results
        [
            {
                "id": "doc2",
                "content": "Holiday policy",
            },
            {
                "id": "doc3",
                "content": "Benefits policy",
            },
        ],
    ]


    fused = reciprocal_rank_fusion(
        results
    )


    assert len(fused) == 3

    # doc2 appears in both lists,
    # therefore should get higher fusion score
    assert fused[0]["id"] == "doc2"
    