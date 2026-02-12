import ast
import builtins

# =========================================================
# GENERIC ANALYZER (SAFE & LANGUAGE-AGNOSTIC)
# =========================================================

SUSPICIOUS_KEYWORDS = ["password", "secret", "token", "apikey", "key"]
DANGEROUS_KEYWORDS = ["eval", "exec", "system", "subprocess"]


def analyze_generic(code: str):
    """
    Lightweight generic checks.
    Avoid deep logic here.
    """
    issues = []
    lowered = code.lower()

    # -----------------------------------------------------
    # Hardcoded secrets (smarter detection)
    # -----------------------------------------------------
    for line in code.splitlines():
        stripped = line.strip()

        if "=" in stripped and not stripped.startswith("#"):
            left, right = stripped.split("=", 1)

            left = left.strip().lower()
            right = right.strip()

            if any(keyword in left for keyword in SUSPICIOUS_KEYWORDS):
                if right.startswith(("\"", "'")):
                    issues.append({
                        "severity": "MEDIUM",
                        "type": "Security",
                        "message": f"Possible hardcoded secret involving '{left}'",
                        "impact": "Credentials may be exposed in source code",
                        "suggestion": "Use environment variables or a secrets manager"
                    })
                    break

    # -----------------------------------------------------
    # Debug statements (generic)
    # -----------------------------------------------------
    if "console.log" in lowered:
        issues.append({
            "severity": "LOW",
            "type": "Code Smell",
            "message": "Debug statement detected",
            "impact": "Debug output should not be present in production code",
            "suggestion": "Use a proper logging framework or remove debug code"
        })

    # -----------------------------------------------------
    # Large file
    # -----------------------------------------------------
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
# PYTHON ANALYZER (AST-BASED SAFE ANALYSIS)
# =========================================================

class PythonCodeAnalyzer(ast.NodeVisitor):

    def __init__(self):
        self.issues = []
        self.builtin_names = set(dir(builtins))

    # -----------------------------------------------------
    # Function length detection
    # -----------------------------------------------------
    def visit_FunctionDef(self, node):
        if hasattr(node, "end_lineno") and node.end_lineno:
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

    # -----------------------------------------------------
    # Dangerous call detection (AST SAFE)
    # -----------------------------------------------------
    def visit_Call(self, node):

        # Direct call like eval()
        if isinstance(node.func, ast.Name):
            func_name = node.func.id

            if func_name in DANGEROUS_KEYWORDS:
                self.issues.append({
                    "severity": "CRITICAL",
                    "type": "Security",
                    "message": f"Dangerous function '{func_name}()' detected",
                    "impact": "May allow arbitrary code execution",
                    "suggestion": "Avoid dynamic execution functions"
                })

            # print detection
            if func_name == "print":
                self.issues.append({
                    "severity": "LOW",
                    "type": "Code Smell",
                    "message": "Use of print() detected",
                    "impact": "Not suitable for production logging",
                    "suggestion": "Use a logging framework instead"
                })

        # Attribute call like os.system()
        elif isinstance(node.func, ast.Attribute):
            attr_name = node.func.attr

            if attr_name in DANGEROUS_KEYWORDS:
                self.issues.append({
                    "severity": "CRITICAL",
                    "type": "Security",
                    "message": f"Dangerous function '{attr_name}()' detected",
                    "impact": "May allow arbitrary code execution",
                    "suggestion": "Avoid dynamic execution mechanisms"
                })

        self.generic_visit(node)

    # -----------------------------------------------------
    # Hardcoded sensitive assignment (AST SAFE)
    # -----------------------------------------------------
    def visit_Assign(self, node):

        for target in node.targets:
            if isinstance(target, ast.Name):

                var_name = target.id.lower()

                if any(keyword in var_name for keyword in SUSPICIOUS_KEYWORDS):

                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
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
            "language": "python",
            "message": f"Python syntax error at line {e.lineno}",
            "impact": "Code will not run",
            "suggestion": "Fix syntax before deployment"
        }]

    analyzer = PythonCodeAnalyzer()
    analyzer.visit(tree)

    return analyzer.issues


# =========================================================
# JAVASCRIPT ANALYZER (HEURISTIC SAFE)
# =========================================================

def analyze_javascript(code: str):

    issues = []
    lowered = code.lower()

    if "process.exit(" in lowered:
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
# MAIN DISPATCHER
# =========================================================

def analyze_code(code: str, language: str):

    issues = []

    # Step 1: Generic rules
    issues.extend(analyze_generic(code))

    # Step 2: Language specific
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
