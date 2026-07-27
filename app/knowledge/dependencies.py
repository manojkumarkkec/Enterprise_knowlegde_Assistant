from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.dependencies import get_db_session

from app.knowledge.repos.document_repository import (
    DocumentRepository,
)

from app.knowledge.services.retriever_service import (
    RetrieverService,
)

from app.knowledge.chat.chat_service import (
    ChatService,
)


def get_document_repository(
    session: AsyncSession = Depends(get_db_session),
) -> DocumentRepository:

    return DocumentRepository(session)


def get_retriever_service(
    session: AsyncSession = Depends(get_db_session),
) -> RetrieverService:

    return RetrieverService(
        session=session,
    )


def get_chat_service(
    session: AsyncSession = Depends(get_db_session),
    retriever_service: RetrieverService = Depends(
        get_retriever_service
    ),
) -> ChatService:

    return ChatService(
        session=session,
        retriever_service=retriever_service,
    )