SEVERITY_WEIGHTS = {
    "CRITICAL": 40,
    "HIGH": 25,
    "MEDIUM": 15,
    "LOW": 5
}

def calculate_risk(issues):
    total_risk = 0
    category_risk = {
        "security": 0,
        "maintainability": 0,
        "performance": 0,
        "readability": 0
    }

    for issue in issues:
        weight = SEVERITY_WEIGHTS.get(issue["severity"], 0)
        total_risk += weight

        issue_type = issue["type"].lower()
        if "security" in issue_type:
            category_risk["security"] += weight
        elif "maintain" in issue_type:
            category_risk["maintainability"] += weight
        elif "performance" in issue_type:
            category_risk["performance"] += weight
        else:
            category_risk["readability"] += weight

    return min(total_risk, 100), category_risk
