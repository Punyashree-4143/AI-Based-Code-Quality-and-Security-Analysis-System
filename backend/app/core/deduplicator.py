# =========================================================
# DEDUPLICATION LAYER
# =========================================================

SEVERITY_RANK = {
    "CRITICAL": 4,
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1
}


def normalize(value: str):
    """
    Normalize strings for safe comparison.
    """
    if not value:
        return ""
    return value.strip().lower()


def extract_target(issue: dict):
    """
    Identify the logical target of an issue.
    Used for deduplication.
    """
    msg = normalize(issue.get("message", ""))

    # Security-related targets
    for key in ["password", "token", "secret", "apikey", "key"]:
        if key in msg:
            return key

    # 🔥 Merge ALL print + debug related LOW issues
    if "print" in msg or "debug" in msg:
        return "print"

    # Dangerous execution
    if any(k in msg for k in ["system", "exec", "eval"]):
        return "dynamic_execution"

    return None


def deduplicate_issues(issues: list):
    """
    Deduplicate issues while preserving the strongest signal.

    Rules:
    - CRITICAL / MEDIUM issues are NEVER removed
    - LOW print/debug issues are merged into one
    - Stronger severity/confidence always wins
    """
    deduped = {}

    for issue in issues:
        # Safety guard
        if not isinstance(issue, dict):
            continue

        severity = normalize(issue.get("severity"))
        issue_type = normalize(issue.get("type"))
        target = extract_target(issue)
        message_key = normalize(issue.get("message", ""))

        # 🔥 SPECIAL RULE:
        # Merge ALL LOW-severity print/debug issues
        if severity == "low" and target == "print":
            key = ("low_print_issue",)
        else:
            key = (issue_type, target or message_key)

        if key not in deduped:
            deduped[key] = issue
            continue

        existing = deduped[key]

        # Compare severity
        existing_sev = SEVERITY_RANK.get(
            existing.get("severity", "").upper(), 0
        )
        new_sev = SEVERITY_RANK.get(
            issue.get("severity", "").upper(), 0
        )

        # Compare confidence
        existing_conf = existing.get("confidence", 0) or 0
        new_conf = issue.get("confidence", 0) or 0

        # Keep stronger issue
        if (
            new_sev > existing_sev
            or (new_sev == existing_sev and new_conf > existing_conf)
        ):
            deduped[key] = issue

    return list(deduped.values())
