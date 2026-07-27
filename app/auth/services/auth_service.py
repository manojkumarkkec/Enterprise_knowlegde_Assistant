from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.auth.models.user import User
from app.auth.repos.role_repository import RoleRepository
from app.auth.repos.user_repository import UserRepository
from app.auth.schemas.user import UserCreate
from app.auth.security.password_token import create_access_token
from app.auth.security.password_token import hash_password, verify_password


class AuthService:

    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session

        self.user_repository = UserRepository(
            session
        )

        self.role_repository = RoleRepository(
            session
        )


    async def create_user(
        self,
        user_data: UserCreate,
    ) -> User:

        # Check duplicate user
        existing_user = await self.user_repository.get_by_email(
            user_data.email
        )

        if existing_user:
            raise ValueError(
                "User already exists"
            )


        # Create user entity
        user = User(
            email=user_data.email,
            hashed_password=hash_password(
                user_data.password
            ),
            role_id=user_data.role_id,
        )


        # Save user
        await self.user_repository.create(
            user
        )


        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

        await self.session.refresh(user)
        return user
    
    async def authenticate(
        self,
        email: str,
        password: str,
    ) -> str:

        user = await self.user_repository.get_by_email(
            email
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )


        password_valid = verify_password(
            password,
            user.hashed_password,
        )

        if not password_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )


        access_token = create_access_token(
            str(user.id)
        )

        return access_token
    
    async def register(
        self,
        email: str,
        password: str,
    ):

        existing = await self.user_repository.get_by_email(email)

        if existing:
            raise ValueError("Email already exists")


        role = await self.role_repository.get_by_name(
            "viewer"
        )

        if role is None:
          raise ValueError("Default role not found")


        user = User(
            email=email,
            hashed_password=hash_password(password),
            role_id=role.id,
        )

        return await self.user_repository.create(user)