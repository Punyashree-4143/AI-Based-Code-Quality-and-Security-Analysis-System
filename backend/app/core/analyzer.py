import ast

# =========================================================
# GENERIC ANALYZER (APPLIES TO ALL LANGUAGES)
# =========================================================

SUSPICIOUS_KEYWORDS = ["password", "secret", "token", "apikey", "key"]
DANGEROUS_KEYWORDS = ["eval(", "exec(", "system(", "os.system", "subprocess"]


def analyze_generic(code: str):
    """
    Language-agnostic checks.
    These run for ALL programming languages.
    """
    issues = []
    lowered = code.lower()

    # Hardcoded secrets
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in lowered and "=" in lowered:
            issues.append({
                "severity": "MEDIUM",
                "type": "Security",
                "message": f"Possible hardcoded secret involving '{keyword}'",
                "impact": "Credentials may be exposed in source code",
                "suggestion": "Use environment variables or a secrets manager"
            })
            break

    # Debug statements
    if "print(" in code or "console.log" in code:
        issues.append({
            "severity": "LOW",
            "type": "Code Smell",
            "message": "Debug statement detected",
            "impact": "Debug output should not be present in production code",
            "suggestion": "Use a proper logging framework or remove debug code"
        })

    # Dangerous execution functions
    for danger in DANGEROUS_KEYWORDS:
        if danger in lowered:
            issues.append({
                "severity": "CRITICAL",
                "type": "Security",
                "message": f"Dangerous function '{danger}' detected",
                "impact": "May allow arbitrary code execution",
                "suggestion": "Avoid dynamic code execution mechanisms"
            })

    # Large file warning
    if len(code.splitlines()) > 500:
        issues.append({
            "severity": "LOW",
            "type": "Maintainability",
            "message": "File is very large",
            "impact": "Large files are harder to maintain and review",
            "suggestion": "Split the file into smaller modules"
        })

    return issues


# =========================================================
# PYTHON ANALYZER
# =========================================================

class PythonCodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.issues = []

    def visit_FunctionDef(self, node):
        length = node.end_lineno - node.lineno + 1

        if length > 30:
            self.issues.append({
                "severity": "MEDIUM",
                "type": "Maintainability",
                "message": f"Function '{node.name}' is too long ({length} lines)",
                "impact": "Hard to maintain and test",
                "suggestion": "Break the function into smaller functions"
            })

        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            self.issues.append({
                "severity": "LOW",
                "type": "Code Smell",
                "message": "Use of print() detected",
                "impact": "Not suitable for production logging",
                "suggestion": "Use a logging framework instead"
            })
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id.lower()
                if any(k in var_name for k in SUSPICIOUS_KEYWORDS):
                    if isinstance(node.value, ast.Constant):
                        self.issues.append({
                            "severity": "CRITICAL",
                            "type": "Security",
                            "message": f"Hardcoded sensitive value assigned to '{target.id}'",
                            "impact": "High risk of credential leakage",
                            "suggestion": "Use environment variables or a secrets manager"
                        })
        self.generic_visit(node)


def analyze_python(code: str):
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [{
            "severity": "CRITICAL",
            "type": "Syntax Error",
            "language": "python",   # 🔥 IMPORTANT FIX
            "message": f"Python syntax error at line {e.lineno}",
            "impact": "Code will not run",
            "suggestion": "Fix syntax before deployment"
        }]

    analyzer = PythonCodeAnalyzer()
    analyzer.visit(tree)
    return analyzer.issues


# =========================================================
# JAVASCRIPT ANALYZER (PARTIAL SUPPORT)
# =========================================================

def analyze_javascript(code: str):
    """
    JavaScript analysis using heuristics only.
    No Python AST is used here.
    """
    issues = []

    if "process.exit" in code:
        issues.append({
            "severity": "CRITICAL",
            "type": "Stability",
            "message": "process.exit() detected",
            "impact": "Calling process.exit() can crash the server",
            "suggestion": "Remove process.exit() from request handlers"
        })

    if "/ 0" in code:
        issues.append({
            "severity": "LOW",
            "type": "Logic",
            "message": "Division by zero detected",
            "impact": "May result in Infinity or invalid output",
            "suggestion": "Validate divisor before division"
        })

    return issues


# =========================================================
# MAIN DISPATCHER (FINAL, LANGUAGE-SAFE)
# =========================================================

def analyze_code(code: str, language: str):
    """
    Main entry point.
    1. Run generic rules (ALL languages)
    2. Run language-specific analyzer
    """
    issues = []

    # Step 1: Generic analysis (always safe)
    issues.extend(analyze_generic(code))

    # Step 2: Language-specific analysis ONLY
    language = language.lower()

    if language == "python":
        issues.extend(analyze_python(code))

    elif language == "javascript":
        issues.extend(analyze_javascript(code))

    else:
        issues.append({
            "severity": "LOW",
            "type": "Unsupported Language",
            "message": f"No deep analysis available for '{language}'",
            "impact": "Only generic checks were applied",
            "suggestion": "Add a language-specific analyzer plugin"
        })

    return issues
