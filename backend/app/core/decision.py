def make_decision(risk_score, issues):
    """
    Decision policy:
    - Any CRITICAL security issue → BLOCK
    - Any other security issue → WARN
    - High overall risk → BLOCK
    - Medium risk → WARN
    - Else → PASS
    """

    # 1️⃣ Hard block: critical security issues
    for issue in issues:
        if issue.get("type") == "Security" and issue.get("severity") == "CRITICAL":
            return "BLOCK"

    # 2️⃣ Soft block: any non-critical security issue
    for issue in issues:
        if issue.get("type") == "Security":
            return "WARN"

    # 3️⃣ Risk score based decision
    if risk_score >= 70:
        return "BLOCK"
    elif risk_score >= 30:
        return "WARN"

    return "PASS"
