from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse

from app.auth.security.jwt_auth import get_current_user
from app.auth.models.user import User
from app.shared.security.rate_limit import limiter

from app.knowledge.chat.chat_service import ChatService
from app.knowledge.dependencies import get_chat_service

from app.knowledge.chat.chat_schema import (
    ChatRequest,
    ChatResponse,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
@limiter.limit("10/minute")
async def chat(
    request: Request,
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    """
    Chat endpoint.
    """

    response = await service.ask(
        question=chat_request.question,
        user_id=str(current_user.id),
        conversation_id=chat_request.conversation_id,
        department=chat_request.department,
        top_k=chat_request.top_k,
    )

    return ChatResponse(
        conversation_id=response["conversation_id"],

        answer=response["answer"],

        sources=response["sources"],

        metrics=response["metrics"],

        usage=response.get("usage"),
    )


@router.post(
    "/stream",
)
async def chat_stream(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    service: ChatService = Depends(get_chat_service),
):
    """
    Streaming chat endpoint (SSE).
    """

    return StreamingResponse(
        service.ask_stream(
            question=request.question,
            user_id=str(current_user.id),
            conversation_id=request.conversation_id,
            department=request.department,
            top_k=request.top_k,
        ),
        media_type="text/event-stream",
    )