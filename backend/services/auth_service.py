from fastapi import HTTPException

from database.models.user import User
from core.security import hash_password


def create_user(
    db,
    name,
    email,
    password
):
    email = email.lower()

    existing_user = get_user_by_email(
        db,
        email
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email is already registered"
        )

    hashed = hash_password(password)

    user = User(
        name=name,
        email=email,
        password=hashed
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_email(
    db,
    email
):
    email = email.lower()

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )
