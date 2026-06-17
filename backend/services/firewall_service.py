def evaluate_firewall(
    risk_score,
    threshold
):

    if risk_score >= threshold:
        return {
            "decision": "BLOCK",
            "reason": (
                f"Risk score exceeded "
                f"threshold {threshold}"
            )
        }

    return {
        "decision": "ALLOW",
        "reason": (
            f"Risk score below "
            f"threshold {threshold}"
        )
    }