from app.core.confidence import calculate_confidence


def enrich_issue(issue, context="deployment"):
    """
    Adds human-readable reasoning and confidence to issues.

    IMPORTANT:
    - Syntax errors are NOT enriched
    - Enrichment respects issue type
    - Security reasoning is contextual
    """

    # 🔥 SYNTAX ERRORS: no enrichment, but ADD confidence
    if issue.get("type") == "Syntax Error":
        enriched = issue.copy()
        enriched["confidence"] = calculate_confidence(issue)
        return enriched

    enriched = issue.copy()

    issue_type = issue.get("type", "").lower()
    severity = issue.get("severity", "").upper()
    message = issue.get("message", "").lower()

    # =================================================
    # SECURITY ISSUES
    # =================================================
    if issue_type == "security" and severity == "CRITICAL":

        # Hardcoded secrets
        if "hardcoded" in message:
            enriched["why_it_matters"] = (
                "Hardcoded secrets can be extracted from source control or logs, "
                "leading to unauthorized system access."
            )

            if context == "interview":
                enriched["interview_impact"] = (
                    "Interviewers usually treat hardcoded credentials as an immediate rejection."
                )

            if context == "deployment":
                enriched["production_risk"] = (
                    "Secrets may leak through logs, crashes, or repository exposure."
                )

        # Dangerous execution
        else:
            enriched["why_it_matters"] = (
                "Dynamic code execution allows attackers to run arbitrary commands, "
                "which can fully compromise the system."
            )

            if context == "interview":
                enriched["interview_impact"] = (
                    "Use of dynamic execution functions indicates poor security awareness."
                )

            if context == "deployment":
                enriched["production_risk"] = (
                    "Attackers could gain full control of the server or underlying system."
                )

    # =================================================
    # MAINTAINABILITY ISSUES
    # =================================================
    elif issue_type == "maintainability":
        enriched["why_it_matters"] = (
            "Poor maintainability increases cognitive load and makes debugging and testing harder."
        )

        enriched["long_term_risk"] = (
            "Over time, this code becomes fragile and costly to modify."
        )

    # =================================================
    # CODE SMELL ISSUES
    # =================================================
    elif issue_type == "code smell":
        enriched["why_it_matters"] = (
            "Code smells indicate shortcuts or poor practices that reduce code quality."
        )

    # =================================================
    # STABILITY / LOGIC ISSUES
    # =================================================
    elif issue_type in ["stability", "logic"]:
        enriched["why_it_matters"] = (
            "Stability issues can cause crashes or unpredictable behavior in production."
        )

    # 🔥 ADD CONFIDENCE (FINAL STEP)
    enriched["confidence"] = calculate_confidence(enriched)

    return enriched
