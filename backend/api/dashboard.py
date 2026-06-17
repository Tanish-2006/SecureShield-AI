from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from database.dependencies import get_db

from services.dashboard_service import (
    get_dashboard_stats,
    get_project_analytics,
    get_category_analytics
)

from core.dependencies import get_current_user
from services.project_service import get_user_project_or_404


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/stats/{project_id}")
def dashboard_stats(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    get_user_project_or_404(
        db,
        project_id,
        current_user.id
    )

    return get_dashboard_stats(
        db,
        project_id
    )


@router.get("/analytics/{project_id}")
def project_analytics(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    get_user_project_or_404(
        db,
        project_id,
        current_user.id
    )

    return get_project_analytics(
        db,
        project_id
    )


@router.get("/categories/{project_id}")
def category_analytics(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    get_user_project_or_404(
        db,
        project_id,
        current_user.id
    )

    return get_category_analytics(
        db,
        project_id
    )
