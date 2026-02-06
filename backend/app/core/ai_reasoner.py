def enrich_issue(issue, context="deployment"):
    enriched = issue.copy()

    issue_type = issue.get("type", "").lower()
    severity = issue.get("severity", "")

    # SECURITY REASONING
    if issue_type == "security" and severity == "CRITICAL":
        enriched["why_it_matters"] = (
            "Hardcoded secrets can be extracted from source control or logs, "
            "leading to unauthorized system access."
        )

        if context == "interview":
            enriched["interview_impact"] = (
                "Interviewers treat hardcoded credentials as an immediate rejection."
            )

        if context == "deployment":
            enriched["production_risk"] = (
                "Secrets may leak through logs, crashes, or repository exposure."
            )

    # MAINTAINABILITY REASONING
    elif issue_type == "maintainability":
        enriched["why_it_matters"] = (
            "Large functions increase cognitive load and make testing and debugging harder."
        )
        enriched["long_term_risk"] = (
            "Future changes are more likely to introduce bugs or regressions."
        )

    # CODE SMELL REASONING
    elif issue_type == "code smell":
        enriched["why_it_matters"] = (
            "Debug statements in production code reduce readability and signal poor practices."
        )

    return enriched
