from app.core.analyzer import analyze_code

def analyze_project(files, language):
    """
    STEP 1:
    - Run existing analyzer on each file
    - NO cross-file logic yet
    """

    project_results = []

    for file in files:
        issues = analyze_code(file.code, language)
        project_results.append({
            "path": file.path,
            "issues": issues
        })

    return project_results
