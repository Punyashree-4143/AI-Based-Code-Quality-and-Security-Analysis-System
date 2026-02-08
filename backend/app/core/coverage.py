def get_language_coverage(language: str):
    """
    Returns analysis coverage percentage for a given language.
    """

    language = language.lower()

    coverage_map = {
        "python": {
            "percent": 90,
            "level": "Full",
            "description": "AST-based deep analysis"
        },
        "javascript": {
            "percent": 60,
            "level": "Partial",
            "description": "Heuristic-based analysis"
        }
    }

    return coverage_map.get(
        language,
        {
            "percent": 30,
            "level": "Generic",
            "description": "Language-agnostic security checks only"
        }
    )
