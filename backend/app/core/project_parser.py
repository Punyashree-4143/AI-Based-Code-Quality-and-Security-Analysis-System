import ast
from collections import defaultdict


class ProjectASTParser(ast.NodeVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.defined_functions = set()
        self.defined_classes = set()
        self.called_functions = set()
        self.imported_names = set()

    # --------------------------------------------------
    # Function definitions
    # --------------------------------------------------
    def visit_FunctionDef(self, node):
        self.defined_functions.add(node.name)
        self.generic_visit(node)

    # --------------------------------------------------
    # Class definitions
    # --------------------------------------------------
    def visit_ClassDef(self, node):
        self.defined_classes.add(node.name)
        self.generic_visit(node)

    # --------------------------------------------------
    # Capture ONLY standalone internal function calls
    # --------------------------------------------------
    def visit_Call(self, node):
        """
        We ONLY collect calls like:
            my_function()

        We IGNORE:
            obj.method()
            module.func()
            router.get()
            list.append()
            string.lower()
            etc.
        """

        if isinstance(node.func, ast.Name):
            self.called_functions.add(node.func.id)

        # Completely ignore Attribute calls
        # That eliminates fake CRITICALs

        self.generic_visit(node)

    # --------------------------------------------------
    # import x
    # --------------------------------------------------
    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name.split(".")[0]
            self.imported_names.add(name)
        self.generic_visit(node)

    # --------------------------------------------------
    # from x import y
    # --------------------------------------------------
    def visit_ImportFrom(self, node):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name
            self.imported_names.add(name)
        self.generic_visit(node)


def parse_project_files(files):
    """
    Input: list of ProjectFile
    Output: project-level symbol table
    """

    project_data = {
        "definitions": defaultdict(list),
        "class_definitions": defaultdict(list),
        "calls": defaultdict(list),
        "imports": set()   # GLOBAL set now
    }

    for file in files:
        try:
            tree = ast.parse(file.code)
        except SyntaxError:
            continue

        parser = ProjectASTParser(file.path)
        parser.visit(tree)

        # Functions
        for fn in parser.defined_functions:
            project_data["definitions"][fn].append(file.path)

        # Classes
        for cls in parser.defined_classes:
            project_data["class_definitions"][cls].append(file.path)

        # Calls
        for fn in parser.called_functions:
            project_data["calls"][fn].append(file.path)

        # Imports (GLOBAL)
        project_data["imports"].update(parser.imported_names)

    return project_data
