from app.core.project_parser import parse_project_files

# Mock ProjectFile-like object
class MockFile:
    def __init__(self, path, code):
        self.path = path
        self.code = code


files = [
    MockFile(
        "main.py",
        "from utils import add\nadd(1, 2)"
    ),
    MockFile(
        "utils.py",
        "def add(a, b):\n    return a + b"
    )
]

result = parse_project_files(files)

print("DEFINITIONS:", dict(result["definitions"]))
print("CALLS:", dict(result["calls"]))
print("IMPORTS:", dict(result["imports"]))
