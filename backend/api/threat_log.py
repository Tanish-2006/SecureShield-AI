from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from database.dependencies import get_db

from core.dependencies import get_current_user

from services.threat_log_service import (
    get_project_threat_logs
)
from services.project_service import get_user_project_or_404

from database.schemas.threat_log import (
    ThreatLogResponse
)

router = APIRouter(
    prefix="/threat-logs",
    tags=["Threat Logs"]
)


@router.get(
    "/{project_id}",
    response_model=list[ThreatLogResponse]
)
def get_threat_logs(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    get_user_project_or_404(
        db,
        project_id,
        current_user.id
    )

    return get_project_threat_logs(
        db,
        project_id
    )
