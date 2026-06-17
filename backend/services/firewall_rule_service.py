from database.models.firewall_rule import FirewallRule


def create_firewall_rule(
    db,
    project_id,
    risk_threshold
):
    existing_rule = get_firewall_rule(
        db,
        project_id
    )

    if existing_rule:
        existing_rule.risk_threshold = risk_threshold
        db.commit()
        db.refresh(existing_rule)
        return existing_rule

    rule = FirewallRule(
        project_id=project_id,
        risk_threshold=risk_threshold
    )

    db.add(rule)
    db.commit()
    db.refresh(rule)

    return rule


def get_firewall_rule(
    db,
    project_id
):

    return db.query(
        FirewallRule
    ).filter(
        FirewallRule.project_id == project_id
    ).first()
