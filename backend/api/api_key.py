from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.dependencies import get_db

from services.project_service import get_user_project_or_404

from database.schemas.api_key import (
    APIKeyCreate,
    APIKeyResponse
)

from services.api_key_service import (
    create_api_key,
    get_api_keys_by_project,
    delete_api_key
)

from core.dependencies import get_current_user

router = APIRouter(
    prefix="/api-keys",
    tags=["API Keys"]
)


@router.post(
    "/",
    response_model=APIKeyResponse
)
def create_new_api_key(
    api_key: APIKeyCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    get_user_project_or_404(
        db,
        api_key.project_id,
        current_user.id
    )

    return create_api_key(
        db,
        api_key.name,
        api_key.provider,
        api_key.api_key,
        api_key.project_id
    )


@router.get("/{project_id}")
def get_project_api_keys(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    get_user_project_or_404(
        db,
        project_id,
        current_user.id
    )

    return get_api_keys_by_project(
        db,
        project_id
    )


@router.delete("/{key_id}")
def revoke_api_key(
    key_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted = delete_api_key(
        db,
        key_id,
        current_user.id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="API key not found or access denied"
        )

    return {"message": "API key revoked successfully"}
