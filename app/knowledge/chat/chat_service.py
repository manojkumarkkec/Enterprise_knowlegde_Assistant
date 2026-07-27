from collections.abc import AsyncGenerator
from time import perf_counter
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.knowledge.chat.citation_formatter import (
    CitationFormatter,
)

from app.knowledge.chat.prompt_builder import (
    PromptBuilder,
)

from app.knowledge.repos.conversation_repository import (
    ConversationRepository,
)

from app.knowledge.services.retriever_service import (
    RetrieverService,
)

from app.shared.ai.azure_openai_client import (
    AzureOpenAIClient,
)

from app.shared.guardrails.input_guard import (
    InputGuard,
)

from app.shared.guardrails.output_guard import (
    OutputGuard,
)

from app.shared.cache.cache_service import (
    CacheService,
)

from app.shared.cache.redis_client import (
    redis_client,
)



class ChatService:


    def __init__(
        self,
        session: AsyncSession,
        retriever_service: RetrieverService,
    ):


        self.session = session

        self.retriever = (
            retriever_service
        )

        self.prompt_builder = (
            PromptBuilder()
        )


        self.conversation_repo = (
            ConversationRepository(
                session
            )
        )


        self.llm = (
            AzureOpenAIClient()
        )


        self.citation_formatter = (
            CitationFormatter()
        )


        self.input_guard = (
            InputGuard()
        )


        self.output_guard = (
            OutputGuard()
        )


        self.cache = CacheService(
            redis_client
        )



    # -----------------------------
    # Source formatter
    # -----------------------------

    def build_sources(
        self,
        contexts: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:


        sources = []


        for item in contexts:


            metadata = item.get(
                "metadata",
                {},
            )


            sources.append(

                {

                    "document_id":
                    metadata.get(
                        "document_id"
                    ),


                    "filename":
                    metadata.get(
                        "filename"
                    ),


                    "chunk_index":
                    metadata.get(
                        "chunk_index"
                    ),


                    "score":
                    metadata.get(
                        "score"
                    ),
                }

            )


        return sources



    # -----------------------------
    # Normal response
    # -----------------------------

    async def ask(
        self,
        question: str,
        user_id: str,
        conversation_id: str | None = None,
        department: str | None = None,
        top_k: int = 5,
    ) -> dict[str, Any]:


        start = perf_counter()


        self.input_guard.validate(
            question
        )


        # conversation

        if conversation_id is None:


            conversation = await (
                self.conversation_repo
                .create(
                    user_id=user_id
                )
            )


            conversation_id = str(
                conversation.id
            )



        history = await (
            self.conversation_repo
            .get_history(
                conversation_id
            )
        )



        # save user message

        await self.conversation_repo.add_message(

            conversation_id,

            "user",

            question,

        )



        # retrieve

        contexts = await (

            self.retriever
            .similarity_search(

                question=question,

                user_id=user_id,

                department=department,

                top_k=top_k,

            )

        )



        if not contexts:


            answer = (
                "I could not find this "
                "information in the knowledge base."
            )


            await self.conversation_repo.add_message(

                conversation_id,

                "assistant",

                answer,

            )


            await self.session.commit()


            return {

                "conversation_id":
                conversation_id,

                "answer":
                answer,

                "sources":
                [],

            }




        messages = (

            self.prompt_builder.build(

                question,

                contexts,

                history,

            )

        )



        result = await (

            self.llm.generate(
                messages
            )

        )


        answer = result["content"]


        answer = (

            self.output_guard
            .sanitize(
                answer
            )

        )



        sources = self.build_sources(
            contexts
        )



        answer = (

            self.citation_formatter
            .format(

                answer,

                sources,

            )

        )



        await self.conversation_repo.add_message(

            conversation_id,

            "assistant",

            answer,

        )



        await self.session.commit()



        return {


            "conversation_id":
            conversation_id,


            "answer":
            answer,


            "sources":
            sources,


            "metrics":

            {

                "total_latency":

                round(

                    perf_counter()
                    -
                    start,

                    3

                )

            }

        }



    # -----------------------------
    # Streaming response
    # -----------------------------

    async def ask_stream(

        self,

        question: str,

        user_id: str,

        conversation_id: str | None = None,

        department: str | None = None,

        top_k: int = 5,

    ) -> AsyncGenerator[str, None]:


        response = await self.ask(

            question,

            user_id,

            conversation_id,

            department,

            top_k,

        )


        for token in response["answer"].split():

            yield (
                f"data: {token} \n\n"
            )


        yield (
            "event: done\n"
            "data: [DONE]\n\n"
        )