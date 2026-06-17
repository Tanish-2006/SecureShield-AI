from sqlalchemy.orm import Session

from database.models.api_key import APIKey
from database.models.project import Project

from core.security import encrypt_api_key


def create_api_key(
    db: Session,
    name: str,
    provider: str,
    api_key: str,
    project_id: int
):

    encrypted = encrypt_api_key(
        api_key
    )

    key = APIKey(
        name=name,
        provider=provider,
        encrypted_key=encrypted,
        project_id=project_id
    )

    db.add(key)
    db.commit()
    db.refresh(key)

    return key


def get_api_keys_by_project(
    db: Session,
    project_id: int
):

    return db.query(
        APIKey
    ).filter(
        APIKey.project_id == project_id
    ).all()


def delete_api_key(
    db: Session,
    key_id: int,
    user_id: int
):

    key = db.query(APIKey).filter(
        APIKey.id == key_id
    ).first()

    if not key:
        return None

    project = db.query(Project).filter(
        Project.id == key.project_id,
        Project.owner_id == user_id
    ).first()

    if not project:
        return None

    db.delete(key)
    db.commit()
    return key