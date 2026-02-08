def make_decision(risk_score, issues):
    """
    Decision policy with trace:
    - Any CRITICAL security issue → BLOCK
    - Any other security issue → WARN
    - High overall risk → BLOCK
    - Medium risk → WARN
    - Else → PASS
    """

    decision_trace = []

    # 1️⃣ Hard block: critical security issues
    for issue in issues:
        if issue.get("type") == "Security" and issue.get("severity") == "CRITICAL":
            decision_trace.append(
                f"Critical security issue: {issue.get('message')}"
            )
            return "BLOCK", decision_trace

        # 🔥 Project-level missing function should BLOCK
        if issue.get("severity") == "CRITICAL" and \
           "used but not defined" in issue.get("message", ""):
            decision_trace.append(
                f"Missing definition: {issue.get('message')}"
            )
            return "BLOCK", decision_trace

    # 2️⃣ Soft block: any non-critical security issue
    for issue in issues:
        if issue.get("type") == "Security":
            decision_trace.append(
                "Non-critical security issues detected"
            )
            return "WARN", decision_trace

    # 3️⃣ Risk score based decision
    if risk_score >= 70:
        decision_trace.append("Overall risk score is high")
        return "BLOCK", decision_trace

    elif risk_score >= 30:
        decision_trace.append("Moderate risk issues detected")
        return "WARN", decision_trace

    decision_trace.append("No high-risk issues detected")
    return "PASS", decision_trace
