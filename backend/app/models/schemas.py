from pydantic import BaseModel
from typing import Optional, Dict, List


# =========================================
# Project-level file representation (NEW)
# =========================================
class ProjectFile(BaseModel):
    path: str
    code: str


# =========================================
# Main Review Request (BACKWARD COMPATIBLE)
# =========================================
class ReviewRequest(BaseModel):
    language: str
    context: Optional[str] = None

    # 🔹 Single-file mode (existing behavior)
    code: Optional[str] = None

    # 🔹 Project-level mode (NEW)
    files: Optional[List[ProjectFile]] = None

    # 🔹 Extra metadata (unchanged)
    metadata: Optional[Dict] = None
