from collections.abc import Sequence
from typing import Any

from openai.types.chat import ChatCompletionMessageParam


SYSTEM_PROMPT = """
You are an enterprise knowledge assistant.

Instructions:

- Answer ONLY using the supplied context.
- Do not use outside knowledge.
- Do not make assumptions.
- If the answer cannot be found in the context, respond exactly:

"I could not find this information in the knowledge base."

- Mention document names when possible.

Previous Conversation:

{history}


Retrieved Context:

{context}
"""


class PromptBuilder:
    """
    Builds RAG prompts.

    Converts:
    - conversation history
    - retrieved documents

    into Azure OpenAI chat messages.
    """


    def build(
        self,
        question: str,
        contexts: Sequence[dict[str, Any]],
        history: Sequence[Any],
    ) -> list[ChatCompletionMessageParam]:

        history_text = self._build_history(
            history
        )


        context_text = self._build_context(
            contexts
        )


        messages: list[
            ChatCompletionMessageParam
        ] = [

            {
                "role": "system",
                "content": SYSTEM_PROMPT.format(
                    history=history_text,
                    context=context_text,
                ),
            },

            {
                "role": "user",
                "content": question,
            },
        ]


        return messages



    def _build_history(
        self,
        history: Sequence[Any],
    ) -> str:

        if not history:
            return "No previous conversation."


        lines = []


        for message in history:

            # SQLAlchemy Message model

            if hasattr(
                message,
                "role"
            ):

                role = (
                    message.role
                    .title()
                )

                content = (
                    message.content
                )


            # dictionary fallback

            else:

                role = (
                    message.get(
                        "role",
                        "Unknown"
                    )
                )

                content = (
                    message.get(
                        "content",
                        ""
                    )
                )


            lines.append(
                f"{role}: {content}"
            )


        return "\n".join(
            lines
        )



    def _build_context(
        self,
        contexts: Sequence[dict[str, Any]],
    ) -> str:


        if not contexts:
            return "No context available."


        sections = []


        for index, item in enumerate(
            contexts,
            start=1,
        ):

            metadata = item.get(
                "metadata",
                {},
            )


            sections.append(
                f"""
========================

Source {index}

Document:
{metadata.get(
    "filename",
    "Unknown"
)}

Chunk:
{metadata.get(
    "chunk_index",
    "Unknown"
)}

Content:

{item.get(
    "content",
    ""
)}

========================
"""
            )


        return "\n".join(
            sections
        )