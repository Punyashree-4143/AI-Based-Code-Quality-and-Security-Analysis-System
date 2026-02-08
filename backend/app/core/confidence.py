def calculate_confidence(issue):
    """
    Returns a confidence score between 0 and 1
    indicating how likely this issue is a real problem.
    """

    severity = issue.get("severity", "").upper()
    issue_type = issue.get("type", "").lower()
    message = issue.get("message", "").lower()

    # Base confidence by severity
    base = {
        "CRITICAL": 0.85,
        "HIGH": 0.75,
        "MEDIUM": 0.6,
        "LOW": 0.4
    }.get(severity, 0.3)

    # Strong signals
    if "hardcoded" in message:
        base += 0.1

    if "dangerous" in message or "system(" in message or "eval" in message:
        base += 0.1

    if "syntax error" in message:
        base = 0.95

    # Generic / heuristic rules → slightly lower confidence
    if issue_type in ["unsupported language", "code smell"]:
        base -= 0.1

    # Clamp
    return round(min(max(base, 0.1), 0.99), 2)
