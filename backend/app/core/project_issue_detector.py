import builtins


def detect_project_issues(project_data):
    """
    Input: project_data from STEP 2
    Output: list of project-level issues
    """

    issues = []

    definitions = project_data["definitions"]
    calls = project_data["calls"]
    imports = project_data.get("imports", set())

    # ==================================================
    # Use REAL Python builtins (not manual list)
    # ==================================================
    PYTHON_BUILTINS = set(dir(builtins))

    # ==================================================
    # 1. Function used but not defined (CRITICAL)
    # ==================================================
    for func_name, call_files in calls.items():

        # Ignore builtins
        if func_name in PYTHON_BUILTINS:
            continue

        # Ignore imported symbols
        if func_name in imports:
            continue

        # Ignore class-like names (Capitalized → likely framework class)
        if func_name and func_name[0].isupper():
            continue

        # Real missing function
        if func_name not in definitions:
            for file in call_files:
                issues.append({
                    "severity": "CRITICAL",
                    "type": "Project Consistency",
                    "message": f"Function '{func_name}' is used but not defined in project",
                    "impact": "Will cause runtime failure",
                    "suggestion": f"Define '{func_name}' or remove its usage",
                    "path": file
                })

    # ==================================================
    # 2. Function defined but never used (Dead Code)
    # ==================================================
    for func_name, def_files in definitions.items():

        if func_name.startswith("_"):
            continue  # ignore private/internal

        if func_name not in calls:
            for file in def_files:
                issues.append({
                    "severity": "LOW",
                    "type": "Dead Code",
                    "message": f"Function '{func_name}' is defined but never used",
                    "impact": "Increases maintenance burden",
                    "suggestion": f"Remove '{func_name}' or use it",
                    "path": file
                })

    # ==================================================
    # 3. Duplicate function definitions
    # ==================================================
    for func_name, def_files in definitions.items():
        if len(def_files) > 1:
            issues.append({
                "severity": "MEDIUM",
                "type": "Duplicate Definition",
                "message": f"Function '{func_name}' is defined in multiple files",
                "impact": "May cause ambiguity or unexpected behavior",
                "suggestion": "Keep a single source of truth",
                "path": ", ".join(def_files)
            })

    return issues
