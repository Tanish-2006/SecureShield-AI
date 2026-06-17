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
    project_id
):

    return db.query(
        ThreatLog
    ).filter(
        ThreatLog.project_id == project_id
    ).all()