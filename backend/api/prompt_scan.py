from sqlalchemy.orm import Session

from database.dependencies import get_db

from services.threat_log_service import (
    create_threat_log
)

from fastapi import APIRouter
from fastapi import Depends

from database.schemas.prompt_scan import (
    PromptScanRequest,
    PromptScanResponse
)

from services.prompt_scan_service import (
    analyze_prompt
)

from core.dependencies import get_current_user
from services.project_service import get_user_project_or_404

router = APIRouter(
    prefix="/prompt-scan",
    tags=["Prompt Security"]
)


@router.post(
    "/",
    response_model=PromptScanResponse
)
def scan_prompt(
    request: PromptScanRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    get_user_project_or_404(
        db,
        request.project_id,
        current_user.id
    )

    result = analyze_prompt(
        request.prompt
    )

    create_threat_log(
        db=db,
        user_id=current_user.id,
        project_id=request.project_id,
        severity=result["severity"],
        threats=result["threats"],
        risk_score=result["risk_score"],
        action=result["action"],
        prompt=request.prompt
    )

    return result
