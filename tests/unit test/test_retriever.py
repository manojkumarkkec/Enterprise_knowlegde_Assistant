import pytest


@pytest.mark.asyncio
async def test_similarity_search():

    class FakeRetriever:


        async def similarity_search(
            self,
            question,
            user_id,
            top_k=5,
        ):

            return [
                {
                    "content":
                    "Security policy",
                    "metadata":
                    {
                        "filename":
                        "security.pdf"
                    }
                }
            ]


    retriever = FakeRetriever()


    result = await retriever.similarity_search(

        question="security",

        user_id="user1",

    )


    assert len(result) == 1


    assert (
        result[0]["metadata"]["filename"]
        ==
        "security.pdf"
    )