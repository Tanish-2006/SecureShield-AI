from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db

from database.schemas.project import (
    ProjectCreate,
    ProjectResponse
)

from services.project_service import (
    create_project,
    get_projects_by_user
)

from core.dependencies import get_current_user

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post(
    "/",
    response_model=ProjectResponse
)
def create_new_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return create_project(
        db,
        project.name,
        project.description,
        current_user.id
    )


@router.get(
    "/",
    response_model=list[ProjectResponse]
)
def get_my_projects(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return get_projects_by_user(
        db,
        current_user.id
    )
