from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.shared.database.session import AsyncSessionLocal
from app.auth.services.auth_service import AuthService


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides one database session per request.
    """
    async with AsyncSessionLocal() as session:
        yield session


def get_auth_service(
    session: AsyncSession = Depends(get_db_session),
) -> AuthService:
    """
    Provides an AuthService instance.
    """
    return AuthService(session=session)