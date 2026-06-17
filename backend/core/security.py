from passlib.context import CryptContext
from jose import jwt
from jose import JWTError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from cryptography.fernet import Fernet

from core.config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


settings.validate_security()

fernet = Fernet(
    settings.ENCRYPTION_KEY.encode()
)


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def verify_token(token: str):

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return payload

    except ExpiredSignatureError:
        raise
    except JWTError:
        return None


def encrypt_api_key(
    api_key: str
):

    return fernet.encrypt(
        api_key.encode()
    ).decode()


def decrypt_api_key(
    encrypted_key: str
):

    return fernet.decrypt(
        encrypted_key.encode()
    ).decode()
