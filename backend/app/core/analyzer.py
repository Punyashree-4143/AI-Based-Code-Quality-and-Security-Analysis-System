import ast

SUSPICIOUS_KEYWORDS = ["password", "secret", "token", "apikey", "key"]

class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.issues = []
        self.function_lengths = []

    def visit_FunctionDef(self, node):
        # Function length check
        length = node.end_lineno - node.lineno + 1
        self.function_lengths.append(length)

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
        # Detect print usage
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
        # Detect hardcoded credentials
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
                            "suggestion": "Use environment variables or secrets manager"
                        })
        self.generic_visit(node)


def analyze_code(code: str):
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return [{
            "severity": "CRITICAL",
            "type": "Syntax Error",
            "message": f"Syntax error at line {e.lineno}",
            "impact": "Code will not run",
            "suggestion": "Fix syntax before deployment"
        }]

    analyzer = CodeAnalyzer()
    analyzer.visit(tree)
    return analyzer.issues
