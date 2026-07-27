from fastapi import FastAPI

from app.auth.routers import auth_router
from app.config.settings import settings
from app.knowledge.routers.document_router import router as document_router
from app.knowledge.chat.chat_router import router as chat_router
from app.shared.observability.langsmith import (
    setup_langsmith,
)
from app.shared.security.rate_limit import limiter


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Enterprise AI Knowledge Assistant API",
)





app.include_router(
    auth_router.router
)

app.include_router(
    document_router
)

app.include_router(
    chat_router,
    prefix="/api/v1"
)