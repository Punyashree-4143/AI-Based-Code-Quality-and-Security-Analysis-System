SEVERITY_WEIGHTS = {
    "CRITICAL": 25,
    "HIGH": 15,
    "MEDIUM": 6,
    "LOW": 2
}


def calculate_risk(issues):
    print("---- DEBUG SCORER START ----")
    print("Total issues received:", len(issues))


    if not issues:
        print("No issues detected. Returning 0.")
        print("---- DEBUG SCORER END ----")
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

        print(f"Issue -> Severity: {severity}, Weight: {weight}, Type: {issue_type}")

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

    print("Total weight:", total_weight)

    # 🔥 Security override
    if security_critical_found:
        print("Security CRITICAL detected → Returning 90")
        print("---- DEBUG SCORER END ----")
        return 90, category_risk

    normalized = total_weight / len(issues)
    final_score = min(int(normalized * 5), 100)

    print("Normalized value:", normalized)
    print("Final static risk:", final_score)
    print("---- DEBUG SCORER END ----")

    return final_score, category_risk
