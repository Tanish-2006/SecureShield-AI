from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database.dependencies import get_db

from core.dependencies import get_current_user

from database.schemas.firewall_rule import (
    FirewallRuleCreate,
    FirewallRuleResponse
)

from services.firewall_rule_service import (
    create_firewall_rule,
    get_firewall_rule
)
from services.project_service import get_user_project_or_404

router = APIRouter(
    prefix="/firewall-rules",
    tags=["Firewall Rules"]
)


@router.post(
    "/",
    response_model=FirewallRuleResponse
)
def create_rule(
    rule: FirewallRuleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    get_user_project_or_404(
        db,
        rule.project_id,
        current_user.id
    )

    return create_firewall_rule(
        db,
        rule.project_id,
        rule.risk_threshold
    )


@router.get(
    "/{project_id}",
    response_model=FirewallRuleResponse
)
def get_rule(
    project_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    get_user_project_or_404(
        db,
        project_id,
        current_user.id
    )

    rule = get_firewall_rule(
        db,
        project_id
    )

    if not rule:
        raise HTTPException(
            status_code=404,
            detail="Firewall rule not found"
        )

    return rule
