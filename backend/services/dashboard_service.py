from database.models.threat_log import ThreatLog


def get_dashboard_stats(
    db,
    project_id
):

    total_threats = db.query(
        ThreatLog
    ).filter(
        ThreatLog.project_id == project_id
    ).count()

    critical = db.query(
        ThreatLog
    ).filter(
        ThreatLog.project_id == project_id,
        ThreatLog.severity == "CRITICAL"
    ).count()

    high = db.query(
        ThreatLog
    ).filter(
        ThreatLog.project_id == project_id,
        ThreatLog.severity == "HIGH"
    ).count()

    medium = db.query(
        ThreatLog
    ).filter(
        ThreatLog.project_id == project_id,
        ThreatLog.severity == "MEDIUM"
    ).count()

    low = db.query(
        ThreatLog
    ).filter(
        ThreatLog.project_id == project_id,
        ThreatLog.severity == "LOW"
    ).count()

    blocked = db.query(
        ThreatLog
    ).filter(
        ThreatLog.project_id == project_id,
        ThreatLog.action == "BLOCK"
    ).count()

    allowed = db.query(
        ThreatLog
    ).filter(
        ThreatLog.project_id == project_id,
        ThreatLog.action == "ALLOW"
    ).count()

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
