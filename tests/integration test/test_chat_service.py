import pytest


@pytest.mark.asyncio
async def test_chat_service_returns_answer(mocker):

    fake_session = mocker.AsyncMock()


    fake_retriever = mocker.Mock()

    fake_retriever.similarity_search = (
        mocker.AsyncMock(
            return_value=[
                {
                    "content": "Company provides 20 leave days.",
                    "metadata": {
                        "filename": "hr.pdf",
                        "chunk_index": 1,
                    }
                }
            ]
        )
    )


    mocker.patch(
        "app.knowledge.chat.chat_service.AzureOpenAIClient"
    )


    from app.knowledge.chat.chat_service import ChatService


    service = ChatService(
        session=fake_session,
        retriever_service=fake_retriever,
    )


    # mock conversation repository

    service.conversation_repo.create = (
        mocker.AsyncMock(
            return_value=mocker.Mock(
                id="123"
            )
        )
    )


    service.conversation_repo.get_history = (
        mocker.AsyncMock(
            return_value=[]
        )
    )


    service.conversation_repo.add_message = (
        mocker.AsyncMock()
    )


    service.llm.generate = (
        mocker.AsyncMock(
            return_value={
                "content":
                    "Company provides 20 leave days.",
                "usage": None,
            }
        )
    )


    response = await service.ask(
        question="Leave policy",
        user_id="test-user",
    )


    assert (
    "Company provides 20 leave days."
    in response["answer"]
    )

    assert (
        "hr.pdf"
        in response["answer"]
    )