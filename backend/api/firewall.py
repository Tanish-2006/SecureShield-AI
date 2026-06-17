from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from database.dependencies import get_db

from database.schemas.firewall import (
    FirewallRequest,
    FirewallResponse
)

from services.prompt_scan_service import (
    analyze_prompt
)

from services.firewall_service import (
    evaluate_firewall
)

from services.firewall_rule_service import (
    get_firewall_rule
)

from core.dependencies import (
    get_current_user
)
from services.project_service import get_user_project_or_404

router = APIRouter(
    prefix="/firewall",
    tags=["Firewall"]
)


@router.post(
    "/",
    response_model=FirewallResponse
)
def firewall_scan(
    request: FirewallRequest,
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

    rule = get_firewall_rule(
        db,
        request.project_id
    )

    threshold = 70

    if rule:
        threshold = rule.risk_threshold

    firewall = evaluate_firewall(
        result["risk_score"],
        threshold
    )

    return {
        "risk_score": result["risk_score"],
        "severity": result["severity"],
        "decision": firewall["decision"],
        "reason": firewall["reason"]
    }
