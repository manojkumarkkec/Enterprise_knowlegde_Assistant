from uuid import UUID

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.auth.models.role import Role
from app.shared.database.session import get_db
from app.auth.models.user import User
from app.auth.repos.user_repository import UserRepository
from app.config.settings import settings
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

algorithms=[
    settings.jwt_algorithm
]


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db),
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        },
    )


    try:

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=algorithms,
        )


        user_id: str | None = payload.get("sub")


        if user_id is None:
            raise credentials_exception


    except JWTError:

        raise credentials_exception


    user_repository = UserRepository(
        session
    )


    stmt = (
    select(User)
    .options(
        selectinload(User.role)
        .selectinload(Role.permissions)
    )
    .where(
        User.id == UUID(user_id)
    )
  )


    user = (await session.execute(stmt)).scalar_one_or_none()


    if user is None:
        raise credentials_exception


    return user