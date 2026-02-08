import ast
from collections import defaultdict


class ProjectASTParser(ast.NodeVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.defined_functions = set()
        self.called_functions = set()
        self.imports = set()

    # -----------------------------
    # Function definitions
    # -----------------------------
    def visit_FunctionDef(self, node):
        self.defined_functions.add(node.name)
        self.generic_visit(node)

    # -----------------------------
    # Function calls
    # -----------------------------
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.called_functions.add(node.func.id)
        self.generic_visit(node)

    # -----------------------------
    # Imports: import x
    # -----------------------------
    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    # -----------------------------
    # Imports: from x import y
    # -----------------------------
    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.add(node.module)
        self.generic_visit(node)


def parse_project_files(files):
    """
    Input: list of ProjectFile
    Output: project-level symbol table
    """

    project_data = {
        "definitions": defaultdict(list),
        "calls": defaultdict(list),
        "imports": defaultdict(list)
    }

    for file in files:
        try:
            tree = ast.parse(file.code)
        except SyntaxError:
            # Syntax errors are already handled by file analyzer
            continue

        parser = ProjectASTParser(file.path)
        parser.visit(tree)

        for fn in parser.defined_functions:
            project_data["definitions"][fn].append(file.path)

        for fn in parser.called_functions:
            project_data["calls"][fn].append(file.path)

        for imp in parser.imports:
            project_data["imports"][imp].append(file.path)

    return project_data
