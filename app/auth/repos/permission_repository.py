from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models.permissions import Permission
from app.auth.models.role import Role


class PermissionRepository:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session


    async def get_role_permissions(
        self,
        role_id,
    ) -> list[Permission]:

        result = await self.session.execute(
            select(Permission)
            .join(Permission.roles)
            .where(
                Role.id == role_id
            )
        )

        return list(
            result.scalars().all()
        )