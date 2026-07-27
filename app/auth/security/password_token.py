from datetime import datetime, timedelta, UTC

from alembic.environment import Any
from jose import jwt
from pwdlib import PasswordHash
from app.config.settings import settings


ALGORITHM = "HS256"


password_hash = PasswordHash.recommended()


def hash_password(
    password: str,
) -> str:

    return password_hash.hash(password)



def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:

    return password_hash.verify(
        plain_password,
        hashed_password,
    )



def create_access_token(
    user_id: str,
) -> str:
    
    """
    Create a signed JWT access token.
    """

    expire = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload : dict[str, Any] = {
        "sub": user_id,
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGORITHM,
    )