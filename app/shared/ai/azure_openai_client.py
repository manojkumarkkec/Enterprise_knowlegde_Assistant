from collections.abc import AsyncGenerator
from typing import Any

from openai import AsyncAzureOpenAI
from openai.types.chat import ChatCompletionMessageParam

from app.config.settings import settings



class AzureOpenAIClient:


    def __init__(self):

        self.client = AsyncAzureOpenAI(

            azure_endpoint=(
                settings.azure_openai_endpoint
            ),

            api_key=(
                settings.azure_openai_key
            ),

            api_version=(
                settings.azure_openai_api_version
            ),

            timeout=60.0,
        )


        self.deployment = (
            settings.azure_openai_deployment
        )



    async def generate(
        self,
        messages: list[ChatCompletionMessageParam],
    ) -> dict[str, Any]:


        response = await (
            self.client
            .chat
            .completions
            .create(

                model=self.deployment,

                messages=messages,

                temperature=0.1,

            )
        )


        content = (
            response
            .choices[0]
            .message
            .content
            or ""
        )


        usage = None


        if response.usage:

            usage = (
                response
                .usage
                .model_dump()
            )


        return {

            "content": content,

            "usage": usage,

        }



    async def stream(
        self,
        messages: list[ChatCompletionMessageParam],
    ) -> AsyncGenerator[str, None]:


        response = await (
            self.client
            .chat
            .completions
            .create(

                model=self.deployment,

                messages=messages,

                temperature=0.2,

                stream=True,

            )
        )


        async for chunk in response:


            delta = (
                chunk
                .choices[0]
                .delta
                .content
            )


            if delta:

                yield delta