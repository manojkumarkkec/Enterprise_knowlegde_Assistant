from fastapi import APIRouter, Depends, status

from app.auth.security.jwt_auth import get_current_user
from app.auth.models.user import User
from app.auth.schemas.register import RegisterRequest, UserResponse
from app.auth.services.auth_service import AuthService
from app.shared.dependencies import get_auth_service
from app.auth.schemas.login import (
    LoginRequest,
    TokenResponse,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
):

    user = await auth_service.register(
        email=request.email,
        password=request.password,
    )

    return UserResponse(
        id=user.id,
        email=user.email,
        role=user.role.name,
    )



@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(
        get_auth_service
    ),
):

    token = await auth_service.authenticate(
        email=request.email,
        password=request.password,
    )


    return TokenResponse(
        access_token=token
    )

@router.get("/me")
async def me(
    current_user: User = Depends(get_current_user),
):

    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "role": current_user.role.name,
    }