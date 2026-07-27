import pytest
from fastapi import HTTPException

from app.auth.security.jwt_auth import get_current_user


@pytest.mark.asyncio
async def test_invalid_token():

    with pytest.raises(HTTPException):

        await get_current_user(
            token="invalid_token"
        )