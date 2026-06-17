from fastapi import Depends
from fastapi import HTTPException
from jose import ExpiredSignatureError

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from core.security import verify_token

from database.dependencies import get_db
from database.models.user import User

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/login",
    auto_error=False
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    try:
        payload = verify_token(token)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    email = payload.get("sub")

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return user