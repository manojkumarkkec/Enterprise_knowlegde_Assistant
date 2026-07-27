from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models.user import User


class UserRepository:
    """
    Handles database operations for users.
    """

    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_email(
        self,
        email: str
    ) -> User | None:

        result = await self.session.execute(
            select(User)
            .where(User.email == email)
        )

        return result.scalar_one_or_none()


    async def create(
        self,
        user: User
    ) -> User:

        self.session.add(user)

        await self.session.flush()

        return user


    async def get_by_id(
        self,
        user_id: UUID
    ) -> User | None:

        result = await self.session.execute(
            select(User)
            .where(User.id == user_id)
        )

        return result.scalar_one_or_none()