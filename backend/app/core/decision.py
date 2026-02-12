def make_decision(risk_score, issues):
    """
    Improved Decision Policy:
    - Critical SECURITY issues → BLOCK
    - Any other CRITICAL issue → WARN
    - Non-critical security issues → WARN
    - High overall risk score → BLOCK
    - Medium risk score → WARN
    - Else → PASS
    """

    decision_trace = []

    # 1️⃣ Hard Block: Critical SECURITY issues
    for issue in issues:
        if issue.get("severity") == "CRITICAL" and issue.get("type") == "Security":
            decision_trace.append(
                f"Critical security issue: {issue.get('message')}"
            )
            return "BLOCK", decision_trace

    # 2️⃣ WARN: Any other CRITICAL issue
    for issue in issues:
        if issue.get("severity") == "CRITICAL":
            decision_trace.append(
                f"Critical issue detected: {issue.get('message')}"
            )
            return "WARN", decision_trace

    # 3️⃣ WARN: Non-critical security issues
    for issue in issues:
        if issue.get("type") == "Security":
            decision_trace.append("Non-critical security issues detected")
            return "WARN", decision_trace

    # 4️⃣ High risk score block
    if risk_score >= 70:
        decision_trace.append("Overall risk score is high")
        return "BLOCK", decision_trace

    # 5️⃣ Medium risk score
    if risk_score >= 30:
        decision_trace.append("Moderate risk issues detected")
        return "WARN", decision_trace

    # 6️⃣ Default PASS
    decision_trace.append("No high-risk issues detected")
    return "PASS", decision_trace
