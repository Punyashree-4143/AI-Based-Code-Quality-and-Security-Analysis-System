def make_decision(risk_score, issues):
    # Hard rule: any critical security issue blocks deployment
    for issue in issues:
        if issue["severity"] == "CRITICAL" and issue["type"] == "Security":
            return "BLOCK"

    if risk_score >= 70:
        return "BLOCK"
    elif risk_score >= 30:
        return "WARN"
    return "PASS"
