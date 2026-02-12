import builtins


def detect_project_issues(project_data):
    """
    Input: project_data from parse_project_files()
    Output: list of project-level issues
    """

    issues = []

    definitions = project_data.get("definitions", {})
    class_definitions = project_data.get("class_definitions", {})
    calls = project_data.get("calls", {})
    imports = project_data.get("imports", {})

    # --------------------------------------------------
    # Collect project-wide imported symbols
    # --------------------------------------------------
    imported_symbols = set(imports.keys())

    # Real Python builtins
    PYTHON_BUILTINS = set(dir(builtins))

    # ==================================================
    # 1. Function used but not defined (CRITICAL)
    # ==================================================
    for func_name, call_files in calls.items():

        if not func_name:
            continue

        # Ignore builtins (round, bool, isinstance, etc.)
        if func_name in PYTHON_BUILTINS:
            continue

        # Ignore imported symbols (load_dotenv, defaultdict, etc.)
        if func_name in imported_symbols:
            continue

        # Ignore class constructors defined in project
        if func_name in class_definitions:
            continue

        # Ignore likely framework classes (FastAPI, APIRouter, etc.)
        if func_name[0].isupper():
            continue

        # Real missing function (internal only)
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

        # Ignore private/internal helpers
        if func_name.startswith("_"):
            continue

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
