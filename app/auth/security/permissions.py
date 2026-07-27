from collections.abc import Callable

from fastapi import Depends, HTTPException, status

from app.auth.security.jwt_auth import get_current_user
from app.auth.models.user import User


def require_permission(permission: str) -> Callable:

    async def checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        permissions = {
            p.name
            for p in current_user.role.permissions
        }

        if permission not in permissions:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )

        return current_user

    return checker