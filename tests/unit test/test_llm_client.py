import pytest
from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_llm_generate_returns_answer(mocker):

    mock_client = mocker.patch(
        "app.shared.ai.azure_openai_client.AsyncAzureOpenAI"
    )


    mock_client.return_value.chat.completions.create = (
        AsyncMock(
            return_value={
                "content":"answer"
            }
        )
    )


    assert True