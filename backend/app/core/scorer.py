SEVERITY_WEIGHTS = {
    "CRITICAL": 25,
    "HIGH": 15,
    "MEDIUM": 6,
    "LOW": 2
}


def calculate_risk(issues):
    if not issues:
        return 0, {}

    total_weight = 0
    category_risk = {
        "security": 0,
        "maintainability": 0,
        "performance": 0,
        "readability": 0
    }

    security_critical_found = False

    for issue in issues:
        severity = issue.get("severity", "LOW")
        issue_type = issue.get("type", "").lower()

        weight = SEVERITY_WEIGHTS.get(severity, 2)
        total_weight += weight

        if severity == "CRITICAL" and "security" in issue_type:
            security_critical_found = True

        if "security" in issue_type:
            category_risk["security"] += weight
        elif "maintain" in issue_type:
            category_risk["maintainability"] += weight
        elif "performance" in issue_type:
            category_risk["performance"] += weight
        else:
            category_risk["readability"] += weight

    # 🔥 Security override
    if security_critical_found:
        return 90, category_risk

    # ✅ Normalize by number of issues
    normalized = total_weight / len(issues)

    # ✅ Scale gently to 0–100 range
    final_score = min(int(normalized * 5), 100)

    return final_score, category_risk
