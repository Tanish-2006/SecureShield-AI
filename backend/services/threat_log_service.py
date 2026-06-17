from database.models.threat_log import ThreatLog


def create_threat_log(
    db,
    user_id,
    project_id,
    severity,
    threats,
    risk_score,
    action,
    prompt
):

    log = ThreatLog(
        user_id=user_id,
        project_id=project_id,
        severity=severity,
        threats=",".join(threats),
        risk_score=risk_score,
        action=action,
        prompt=prompt
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log  


def get_project_threat_logs(
    db,
    project_id,
    skip: int = 0,
    limit: int = 100
):

    return db.query(
        ThreatLog
    ).filter(
        ThreatLog.project_id == project_id
    ).order_by(
        ThreatLog.created_at.desc()
    ).offset(skip).limit(limit).all()


def count_project_threat_logs(
    db,
    project_id
):

    return db.query(
        ThreatLog
    ).filter(
        ThreatLog.project_id == project_id
    ).count()