from sqlalchemy import func

from database.models.threat_log import ThreatLog


def get_dashboard_stats(
    db,
    project_id
):

    from sqlalchemy import text

    rows = db.query(
        ThreatLog.severity,
        ThreatLog.action,
        func.count(ThreatLog.id).label("cnt")
    ).filter(
        ThreatLog.project_id == project_id
    ).group_by(
        ThreatLog.severity,
        ThreatLog.action
    ).all()

    severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    action_counts = {"BLOCK": 0, "ALLOW": 0}
    total_threats = 0

    for severity, action, cnt in rows:
        severity_counts[severity] = severity_counts.get(severity, 0) + cnt
        action_counts[action] = action_counts.get(action, 0) + cnt
        total_threats += cnt

    critical = severity_counts.get("CRITICAL", 0)
    high = severity_counts.get("HIGH", 0)
    medium = severity_counts.get("MEDIUM", 0)
    low = severity_counts.get("LOW", 0)
    blocked = action_counts.get("BLOCK", 0)
    allowed = action_counts.get("ALLOW", 0)

    total_weighted = critical * 30 + high * 15 + medium * 5
    security_score = max(0, 100 - total_weighted)
    if total_threats == 0:
        security_score = 100

    return {
        "project_id": project_id,
        "total_threats": total_threats,
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low,
        "blocked": blocked,
        "allowed": allowed,
        "security_score": security_score
    }


def get_project_analytics(
    db,
    project_id
):

    threats = db.query(
        ThreatLog
    ).filter(
        ThreatLog.project_id == project_id
    )

    total_threats = threats.count()

    critical = threats.filter(
        ThreatLog.severity == "CRITICAL"
    ).count()

    high = threats.filter(
        ThreatLog.severity == "HIGH"
    ).count()

    medium = threats.filter(
        ThreatLog.severity == "MEDIUM"
    ).count()

    low = threats.filter(
        ThreatLog.severity == "LOW"
    ).count()

    blocked = threats.filter(
        ThreatLog.action == "BLOCK"
    ).count()

    allowed = threats.filter(
        ThreatLog.action == "ALLOW"
    ).count()

    return {
        "project_id": project_id,
        "total_threats": total_threats,
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low,
        "blocked": blocked,
        "allowed": allowed
    }


def get_category_analytics(
    db,
    project_id
):

    logs = db.query(
        ThreatLog
    ).filter(
        ThreatLog.project_id == project_id
    ).all()

    categories = {}

    for log in logs:

        threats = log.threats.split(",")

        for threat in threats:

            threat = threat.strip()

            categories[threat] = (
                categories.get(threat, 0) + 1
            )

    return categories
