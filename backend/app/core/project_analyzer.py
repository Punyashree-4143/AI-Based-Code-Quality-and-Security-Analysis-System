from app.core.analyzer import analyze_code
from app.core.project_parser import parse_project_files
from app.core.project_issue_detector import detect_project_issues


def analyze_project(files, language):
    """
    STEP 3:
    - File-level analysis (existing)
    - Project-level parsing (AST)
    - Cross-file issue detection
    """

    project_results = []

    # -----------------------------------
    # File-level analysis (existing)
    # -----------------------------------
    for file in files:
        issues = analyze_code(file.code, language)
        project_results.append({
            "path": file.path,
            "issues": issues
        })

    # -----------------------------------
    # Project-level AST parsing (STEP 2)
    # -----------------------------------
    project_data = parse_project_files(files)

    # -----------------------------------
    # Cross-file issue detection (STEP 3)
    # -----------------------------------
    project_issues = detect_project_issues(project_data)

    # -----------------------------------
    # Attach project-level issues
    # -----------------------------------
    project_results.append({
        "path": "__project__",
        "issues": project_issues
    })

    return project_results
